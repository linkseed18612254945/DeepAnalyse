"""Knowledge Graph Builder.

Manages entities and relationships extracted during retrieval rounds.
Provides an in-memory graph with optional Neo4j persistence for queryable,
visually explorable entity networks.
"""

from __future__ import annotations

import logging
from typing import Any

from backend.app.core.models import (
    ConfidenceLevel,
    Entity,
    Relationship,
    RelationshipType,
)

logger = logging.getLogger(__name__)


class KnowledgeGraph:
    """In-memory knowledge graph with merge and query capabilities."""

    def __init__(self) -> None:
        self._entities: dict[str, Entity] = {}
        self._relationships: dict[str, Relationship] = {}
        # Adjacency: entity_id -> list of relationship ids
        self._adjacency: dict[str, list[str]] = {}

    # ------------------------------------------------------------------
    # Entity operations
    # ------------------------------------------------------------------

    def add_entity(self, entity: Entity) -> Entity:
        """Add or merge an entity into the graph."""
        existing = self._find_by_name(entity.name, entity.entity_type)
        if existing:
            # Merge attributes and sources
            existing.attributes.update(entity.attributes)
            existing.sources.extend(entity.sources)
            if entity.description and not existing.description:
                existing.description = entity.description
            return existing
        self._entities[entity.id] = entity
        self._adjacency.setdefault(entity.id, [])
        return entity

    def get_entity(self, entity_id: str) -> Entity | None:
        return self._entities.get(entity_id)

    def get_all_entities(self) -> list[Entity]:
        return list(self._entities.values())

    def find_entities_by_type(self, entity_type: str) -> list[Entity]:
        return [e for e in self._entities.values() if e.entity_type == entity_type]

    # ------------------------------------------------------------------
    # Relationship operations
    # ------------------------------------------------------------------

    def add_relationship(self, rel: Relationship) -> Relationship:
        """Add a relationship to the graph."""
        # Avoid exact duplicates
        for existing in self._relationships.values():
            if (
                existing.source_entity_id == rel.source_entity_id
                and existing.target_entity_id == rel.target_entity_id
                and existing.relationship_type == rel.relationship_type
            ):
                existing.sources.extend(rel.sources)
                return existing

        self._relationships[rel.id] = rel
        self._adjacency.setdefault(rel.source_entity_id, []).append(rel.id)
        self._adjacency.setdefault(rel.target_entity_id, []).append(rel.id)
        return rel

    def get_relationships_for(self, entity_id: str) -> list[Relationship]:
        """Return all relationships involving a given entity."""
        rel_ids = self._adjacency.get(entity_id, [])
        return [self._relationships[rid] for rid in rel_ids if rid in self._relationships]

    def get_all_relationships(self) -> list[Relationship]:
        return list(self._relationships.values())

    # ------------------------------------------------------------------
    # Graph queries
    # ------------------------------------------------------------------

    def get_neighbours(self, entity_id: str, depth: int = 1) -> list[Entity]:
        """BFS to find entities within N hops."""
        visited: set[str] = {entity_id}
        frontier: set[str] = {entity_id}

        for _ in range(depth):
            next_frontier: set[str] = set()
            for eid in frontier:
                for rel in self.get_relationships_for(eid):
                    for neighbour_id in (rel.source_entity_id, rel.target_entity_id):
                        if neighbour_id not in visited:
                            visited.add(neighbour_id)
                            next_frontier.add(neighbour_id)
            frontier = next_frontier

        return [self._entities[eid] for eid in visited if eid in self._entities and eid != entity_id]

    def to_dict(self) -> dict[str, Any]:
        """Serialise the graph for API responses / frontend consumption."""
        return {
            "entities": [e.model_dump() for e in self._entities.values()],
            "relationships": [r.model_dump() for r in self._relationships.values()],
        }

    @property
    def entity_count(self) -> int:
        return len(self._entities)

    @property
    def relationship_count(self) -> int:
        return len(self._relationships)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _find_by_name(self, name: str, entity_type: str) -> Entity | None:
        name_lower = name.lower()
        for e in self._entities.values():
            if e.name.lower() == name_lower and e.entity_type == entity_type:
                return e
        return None


class Neo4jGraphStore:
    """Optional persistent store backed by Neo4j.

    Only used when Neo4j credentials are configured.  Falls back gracefully
    to in-memory-only mode.
    """

    def __init__(self, uri: str, user: str, password: str) -> None:
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None

    async def connect(self) -> bool:
        try:
            from neo4j import AsyncGraphDatabase
            self._driver = AsyncGraphDatabase.driver(
                self._uri, auth=(self._user, self._password)
            )
            # Test connectivity
            async with self._driver.session() as session:
                await session.run("RETURN 1")
            logger.info("Connected to Neo4j at %s", self._uri)
            return True
        except Exception as e:
            logger.warning("Neo4j unavailable, using in-memory graph only: %s", e)
            self._driver = None
            return False

    async def sync_graph(self, graph: KnowledgeGraph) -> None:
        """Push the in-memory graph to Neo4j."""
        if not self._driver:
            return

        async with self._driver.session() as session:
            for entity in graph.get_all_entities():
                await session.run(
                    "MERGE (e:Entity {id: $id}) "
                    "SET e.name = $name, e.type = $type, e.description = $desc",
                    id=entity.id,
                    name=entity.name,
                    type=entity.entity_type,
                    desc=entity.description,
                )

            for rel in graph.get_all_relationships():
                await session.run(
                    "MATCH (a:Entity {id: $src}), (b:Entity {id: $tgt}) "
                    "MERGE (a)-[r:RELATED {id: $rid}]->(b) "
                    "SET r.type = $rtype, r.description = $desc",
                    src=rel.source_entity_id,
                    tgt=rel.target_entity_id,
                    rid=rel.id,
                    rtype=rel.relationship_type,
                    desc=rel.description,
                )

    async def close(self) -> None:
        if self._driver:
            await self._driver.close()
