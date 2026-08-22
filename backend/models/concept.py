from sqlalchemy import Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base

class Concept(Base):
    __tablename__ = "concepts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    class_level: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[str] = mapped_column(String, nullable=False)  # 'easy', 'medium', 'hard'
    learning_objectives: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    # Relationships
    relationships_out = relationship(
        "ConceptRelationship",
        foreign_keys="ConceptRelationship.source_concept_id",
        back_populates="source_concept",
        cascade="all, delete-orphan"
    )
    relationships_in = relationship(
        "ConceptRelationship",
        foreign_keys="ConceptRelationship.target_concept_id",
        back_populates="target_concept",
        cascade="all, delete-orphan"
    )

class ConceptRelationship(Base):
    __tablename__ = "concept_relationships"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_concept_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False
    )
    target_concept_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False
    )
    relationship_type: Mapped[str] = mapped_column(
        String, default="prerequisite_for", nullable=False  # 'prerequisite_for', 'related_to', 'part_of'
    )

    source_concept = relationship(
        "Concept",
        foreign_keys=[source_concept_id],
        back_populates="relationships_out"
    )
    target_concept = relationship(
        "Concept",
        foreign_keys=[target_concept_id],
        back_populates="relationships_in"
    )
