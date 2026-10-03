"""External-revision application and immutable specification versioning.

The service validates identity and structural authority only.  It never
generates replacement text, selects a bound, or decides whether a revision is
effective.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum

from ..domain import Requirement
from ..dynamic_evidence import FullModelStatus
from ..metrics import ArtifactRef, ContractRef, RequirementSubjectRef, RuleRef, RuleVersionAuthority
from .domain import (
    PROCESS_REASSESSMENT_CONTRACT_REF,
    ActionApplicationId,
    ActionApplicationRef,
    ActionRef,
    CorrectiveAction,
    CorrectiveActionStatus,
    RequirementLineageId,
    RevisionRef,
    _identifier,
    _typed_tuple,
    _unique,
)


APPLICATION_RULE_REF = RuleRef(
    "APPLY-EXTERNAL-REVISION-001",
    "1",
    RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
)


class ExternalRevisionProviderKind(str, Enum):
    STAKEHOLDER = "STAKEHOLDER"
    CONTROLLED_REFERENCE_FIXTURE = "CONTROLLED_REFERENCE_FIXTURE"


class RequirementChangeKind(str, Enum):
    REPLACE_TEXT = "REPLACE_TEXT"


class ActionApplicationReason(str, Enum):
    EXTERNAL_REVISION_MATERIALIZED = "EXTERNAL_REVISION_MATERIALIZED"


@dataclass(frozen=True, slots=True, order=True)
class ExternalProviderRef:
    provider_id: str
    provider_version: str

    def __post_init__(self) -> None:
        _identifier(self.provider_id, "provider_id")
        _identifier(self.provider_version, "provider_version")


@dataclass(frozen=True, slots=True, order=True)
class RequirementTextReplacement:
    lineage_id: RequirementLineageId
    expected_parent_subject_ref: RequirementSubjectRef
    replacement_text: str

    def __post_init__(self) -> None:
        if not isinstance(self.lineage_id, RequirementLineageId):
            raise TypeError("lineage_id must be a RequirementLineageId")
        if not isinstance(self.expected_parent_subject_ref, RequirementSubjectRef):
            raise TypeError(
                "expected_parent_subject_ref must be a RequirementSubjectRef"
            )
        if not isinstance(self.replacement_text, str):
            raise TypeError("replacement_text must be a string")
        try:
            self.replacement_text.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise ValueError("replacement_text must be valid UTF-8") from exc
        if (
            not self.replacement_text
            or self.replacement_text != self.replacement_text.strip()
            or "\n" in self.replacement_text
            or "\r" in self.replacement_text
        ):
            raise ValueError(
                "replacement_text must be non-empty, trimmed, and contain no line break"
            )


@dataclass(frozen=True, slots=True)
class ExternalRevisionProvenance:
    revision_ref: RevisionRef
    action_ref: ActionRef
    parent_artifact_ref: ArtifactRef
    requested_child_artifact_ref: ArtifactRef
    provider_ref: ExternalProviderRef
    process_reassessment_contract_ref: ContractRef = PROCESS_REASSESSMENT_CONTRACT_REF
    application_rule_ref: RuleRef = APPLICATION_RULE_REF

    def __post_init__(self) -> None:
        if self.process_reassessment_contract_ref != PROCESS_REASSESSMENT_CONTRACT_REF:
            raise ValueError("external revision requires the process contract")
        if self.application_rule_ref != APPLICATION_RULE_REF:
            raise ValueError("external revision requires the application rule")


@dataclass(frozen=True, slots=True)
class ExternallySuppliedRevision:
    revision_id: str
    revision_version: str
    provider_kind: ExternalRevisionProviderKind
    provider_ref: ExternalProviderRef
    action_ref: ActionRef
    parent_artifact_ref: ArtifactRef
    requested_child_artifact_ref: ArtifactRef
    replacements: tuple[RequirementTextReplacement, ...]
    provider_rationale_or_none: str | None
    provenance: ExternalRevisionProvenance

    def __post_init__(self) -> None:
        _identifier(self.revision_id, "revision_id")
        _identifier(self.revision_version, "revision_version")
        if not isinstance(self.provider_kind, ExternalRevisionProviderKind):
            raise TypeError("provider_kind must be an ExternalRevisionProviderKind")
        if not isinstance(self.provider_ref, ExternalProviderRef):
            raise TypeError("provider_ref must be an ExternalProviderRef")
        _typed_tuple(self.replacements, RequirementTextReplacement, "replacements")
        if not self.replacements:
            raise ValueError("an external revision requires at least one replacement")
        _unique(tuple(item.lineage_id for item in self.replacements), "replacement lineages")
        if self.provider_rationale_or_none is not None:
            _identifier(self.provider_rationale_or_none, "provider_rationale_or_none")
        if self.provenance != ExternalRevisionProvenance(
            self.ref,
            self.action_ref,
            self.parent_artifact_ref,
            self.requested_child_artifact_ref,
            self.provider_ref,
        ):
            raise ValueError("external-revision provenance does not match the revision")

    @property
    def ref(self) -> RevisionRef:
        return RevisionRef(self.revision_id, self.revision_version)


@dataclass(frozen=True, slots=True, order=True)
class VersionedRequirement:
    lineage_id: RequirementLineageId
    subject_ref: RequirementSubjectRef
    text: str
    predecessor_subject_ref: RequirementSubjectRef | None

    def __post_init__(self) -> None:
        if not isinstance(self.lineage_id, RequirementLineageId):
            raise TypeError("lineage_id must be a RequirementLineageId")
        if not isinstance(self.subject_ref, RequirementSubjectRef):
            raise TypeError("subject_ref must be a RequirementSubjectRef")
        Requirement(self.subject_ref.requirement_id, self.subject_ref.source_line, self.text)
        if self.lineage_id.artifact_id != self.subject_ref.artifact_ref.artifact_id:
            raise ValueError("lineage and subject must belong to the same artifact")
        if self.predecessor_subject_ref is not None and not isinstance(
            self.predecessor_subject_ref, RequirementSubjectRef
        ):
            raise TypeError("predecessor_subject_ref must be a RequirementSubjectRef")


@dataclass(frozen=True, slots=True, order=True)
class ChangedRequirementSubject:
    lineage_id: RequirementLineageId
    before_subject_ref: RequirementSubjectRef
    after_subject_ref: RequirementSubjectRef
    change_kind: RequirementChangeKind = RequirementChangeKind.REPLACE_TEXT

    def __post_init__(self) -> None:
        if not isinstance(self.lineage_id, RequirementLineageId):
            raise TypeError("lineage_id must be a RequirementLineageId")
        if self.change_kind is not RequirementChangeKind.REPLACE_TEXT:
            raise ValueError("only REPLACE_TEXT is supported")
        if (
            self.before_subject_ref.artifact_ref.artifact_id != self.lineage_id.artifact_id
            or self.after_subject_ref.artifact_ref.artifact_id != self.lineage_id.artifact_id
        ):
            raise ValueError("changed subjects must preserve artifact lineage")


@dataclass(frozen=True, slots=True)
class SpecificationVersionProvenance:
    artifact_ref: ArtifactRef
    parent_artifact_ref: ArtifactRef | None
    application_ref: ActionApplicationRef | None
    revision_ref: RevisionRef | None
    process_reassessment_contract_ref: ContractRef = PROCESS_REASSESSMENT_CONTRACT_REF
    application_rule_ref_or_none: RuleRef | None = None

    def __post_init__(self) -> None:
        if self.process_reassessment_contract_ref != PROCESS_REASSESSMENT_CONTRACT_REF:
            raise ValueError("specification version requires the process contract")
        if self.parent_artifact_ref is None:
            if any(
                item is not None
                for item in (
                    self.application_ref,
                    self.revision_ref,
                    self.application_rule_ref_or_none,
                )
            ):
                raise ValueError("an initial version has no application provenance")
        elif (
            self.application_ref is None
            or self.revision_ref is None
            or self.application_rule_ref_or_none != APPLICATION_RULE_REF
        ):
            raise ValueError("a child version requires complete application provenance")


@dataclass(frozen=True, slots=True)
class SpecificationVersion:
    artifact_ref: ArtifactRef
    parent_artifact_ref: ArtifactRef | None
    created_by_application_ref: ActionApplicationRef | None
    requirements: tuple[VersionedRequirement, ...]
    changed_subjects: tuple[ChangedRequirementSubject, ...]
    provenance: SpecificationVersionProvenance

    def __post_init__(self) -> None:
        _typed_tuple(self.requirements, VersionedRequirement, "requirements")
        _typed_tuple(self.changed_subjects, ChangedRequirementSubject, "changed_subjects")
        if not self.requirements:
            raise ValueError("a specification version requires at least one requirement")
        subjects = tuple(item.subject_ref for item in self.requirements)
        lineages = tuple(item.lineage_id for item in self.requirements)
        _unique(subjects, "requirement subjects")
        _unique(lineages, "requirement lineages")
        if any(item.subject_ref.artifact_ref != self.artifact_ref for item in self.requirements):
            raise ValueError("requirements cannot cross artifact versions")
        expected_order = tuple(
            sorted(subjects, key=lambda item: (item.source_line, item.requirement_id))
        )
        if subjects != expected_order:
            raise ValueError("requirements must use deterministic source order")
        if self.provenance != SpecificationVersionProvenance(
            self.artifact_ref,
            self.parent_artifact_ref,
            self.created_by_application_ref,
            self.provenance.revision_ref,
            application_rule_ref_or_none=(
                None if self.parent_artifact_ref is None else APPLICATION_RULE_REF
            ),
        ):
            raise ValueError("specification-version provenance is inconsistent")
        if self.parent_artifact_ref is None:
            if self.created_by_application_ref is not None or self.changed_subjects:
                raise ValueError("an initial version has no application or changed subjects")
            if any(item.predecessor_subject_ref is not None for item in self.requirements):
                raise ValueError("initial requirements have no predecessor subjects")
        else:
            if (
                self.created_by_application_ref is None
                or self.parent_artifact_ref.artifact_id != self.artifact_ref.artifact_id
                or self.parent_artifact_ref.artifact_version
                == self.artifact_ref.artifact_version
                or not self.changed_subjects
            ):
                raise ValueError("a child must have one distinct parent and changed subjects")


@dataclass(frozen=True, slots=True)
class ApplicationIdentityContext:
    application_instance_id: str
    application_version: str
    applied_action_record_version: str
    transition_instance_id: str

    def __post_init__(self) -> None:
        _identifier(self.application_instance_id, "application_instance_id")
        _identifier(self.application_version, "application_version")
        _identifier(self.applied_action_record_version, "applied_action_record_version")
        _identifier(self.transition_instance_id, "transition_instance_id")


@dataclass(frozen=True, slots=True, order=True)
class ArtifactTransitionId:
    transition_instance_id: str
    application_ref: ActionApplicationRef

    def __post_init__(self) -> None:
        _identifier(self.transition_instance_id, "transition_instance_id")


@dataclass(frozen=True, slots=True)
class ArtifactTransitionProvenance:
    action_before_ref: ActionRef
    action_after_ref: ActionRef
    application_ref: ActionApplicationRef
    revision_ref: RevisionRef
    process_reassessment_contract_ref: ContractRef = PROCESS_REASSESSMENT_CONTRACT_REF
    application_rule_ref: RuleRef = APPLICATION_RULE_REF

    def __post_init__(self) -> None:
        if self.application_ref.application_id.action_before_ref != self.action_before_ref:
            raise ValueError("transition provenance action-before identity is inconsistent")
        if self.application_ref.application_id.revision_ref != self.revision_ref:
            raise ValueError("transition provenance revision identity is inconsistent")
        if self.process_reassessment_contract_ref != PROCESS_REASSESSMENT_CONTRACT_REF:
            raise ValueError("transition provenance requires the process contract")
        if self.application_rule_ref != APPLICATION_RULE_REF:
            raise ValueError("transition provenance requires the application rule")


@dataclass(frozen=True, slots=True)
class ArtifactTransition:
    transition_id: ArtifactTransitionId
    parent_artifact_ref: ArtifactRef
    child_artifact_ref: ArtifactRef
    action_application_ref: ActionApplicationRef
    revision_ref: RevisionRef
    changed_subjects: tuple[ChangedRequirementSubject, ...]
    provenance: ArtifactTransitionProvenance

    def __post_init__(self) -> None:
        if self.transition_id.application_ref != self.action_application_ref:
            raise ValueError("transition identity must preserve the application ref")
        if self.parent_artifact_ref == self.child_artifact_ref:
            raise ValueError("transition parent and child must be distinct")
        if (
            self.parent_artifact_ref.artifact_id
            != self.child_artifact_ref.artifact_id
        ):
            raise ValueError("transition must preserve stable artifact identity")
        if (
            self.action_application_ref.application_id.child_artifact_ref
            != self.child_artifact_ref
        ):
            raise ValueError("transition child must match the application identity")
        if self.action_application_ref.application_id.revision_ref != self.revision_ref:
            raise ValueError("transition revision must match the application identity")
        _typed_tuple(self.changed_subjects, ChangedRequirementSubject, "changed_subjects")
        if not self.changed_subjects:
            raise ValueError("transition requires the non-empty replacement set")
        if (
            self.provenance.application_ref != self.action_application_ref
            or self.provenance.revision_ref != self.revision_ref
        ):
            raise ValueError("transition provenance is inconsistent")


@dataclass(frozen=True, slots=True)
class ActionApplicationProvenance:
    action_before_ref: ActionRef
    action_after_ref: ActionRef
    revision_ref: RevisionRef
    provider_ref: ExternalProviderRef
    parent_artifact_ref: ArtifactRef
    child_artifact_ref: ArtifactRef
    application_rule_ref: RuleRef = APPLICATION_RULE_REF
    process_reassessment_contract_ref: ContractRef = PROCESS_REASSESSMENT_CONTRACT_REF

    def __post_init__(self) -> None:
        if self.application_rule_ref != APPLICATION_RULE_REF:
            raise ValueError("application provenance requires the application rule")
        if self.process_reassessment_contract_ref != PROCESS_REASSESSMENT_CONTRACT_REF:
            raise ValueError("application provenance requires the process contract")


@dataclass(frozen=True, slots=True)
class ActionApplication:
    application_id: ActionApplicationId
    application_version: str
    action_before_ref: ActionRef
    action_after_ref: ActionRef
    revision_ref: RevisionRef
    parent_artifact_ref: ArtifactRef
    child_artifact_ref: ArtifactRef
    changed_subjects: tuple[ChangedRequirementSubject, ...]
    rule_ref: RuleRef
    status: FullModelStatus
    reason_codes: tuple[ActionApplicationReason, ...]
    provenance: ActionApplicationProvenance
    applied_action: CorrectiveAction
    child_specification: SpecificationVersion
    transition: ArtifactTransition

    def __post_init__(self) -> None:
        _identifier(self.application_version, "application_version")
        if self.status is not FullModelStatus.AVAILABLE:
            raise ValueError("materialized ActionApplication must be AVAILABLE")
        if self.rule_ref != APPLICATION_RULE_REF:
            raise ValueError("application requires APPLY-EXTERNAL-REVISION-001 / 1")
        if self.application_id != ActionApplicationId(
            self.application_id.application_instance_id,
            self.action_before_ref,
            self.revision_ref,
            self.child_artifact_ref,
        ):
            raise ValueError("application_id must be the structured application identity")
        _typed_tuple(self.changed_subjects, ChangedRequirementSubject, "changed_subjects")
        if not self.changed_subjects:
            raise ValueError("available application requires changed subjects")
        if self.applied_action.status is not CorrectiveActionStatus.APPLIED:
            raise ValueError("application must contain the APPLIED action version")
        if self.applied_action.ref != self.action_after_ref:
            raise ValueError("action_after_ref must identify applied_action")
        if self.child_specification.artifact_ref != self.child_artifact_ref:
            raise ValueError("child artifact and specification must agree")
        if self.transition.action_application_ref != self.ref:
            raise ValueError("transition must identify this application")
        if (
            self.transition.parent_artifact_ref != self.parent_artifact_ref
            or self.transition.child_artifact_ref != self.child_artifact_ref
            or self.transition.revision_ref != self.revision_ref
            or self.transition.changed_subjects != self.changed_subjects
        ):
            raise ValueError("application and artifact transition must agree")
        if (
            self.child_specification.parent_artifact_ref != self.parent_artifact_ref
            or self.child_specification.created_by_application_ref != self.ref
            or self.child_specification.changed_subjects != self.changed_subjects
        ):
            raise ValueError("application and child specification must agree")
        if self.provenance != ActionApplicationProvenance(
            self.action_before_ref,
            self.action_after_ref,
            self.revision_ref,
            self.provenance.provider_ref,
            self.parent_artifact_ref,
            self.child_artifact_ref,
        ):
            raise ValueError("application provenance is inconsistent")

    @property
    def ref(self) -> ActionApplicationRef:
        return ActionApplicationRef(self.application_id, self.application_version)


def create_initial_specification_version(
    artifact_ref: ArtifactRef,
    requirements: tuple[Requirement, ...],
) -> SpecificationVersion:
    """Materialize an accepted initial artifact with origin-tuple lineages."""

    if not isinstance(artifact_ref, ArtifactRef):
        raise TypeError("artifact_ref must be an ArtifactRef")
    _typed_tuple(requirements, Requirement, "requirements")
    versioned = tuple(
        VersionedRequirement(
            RequirementLineageId(
                artifact_ref.artifact_id,
                artifact_ref.artifact_version,
                item.id,
                item.source_line,
            ),
            RequirementSubjectRef(artifact_ref, item.id, item.source_line),
            item.text,
            None,
        )
        for item in requirements
    )
    provenance = SpecificationVersionProvenance(
        artifact_ref, None, None, None
    )
    return SpecificationVersion(artifact_ref, None, None, versioned, (), provenance)


def apply_external_revision(
    action: CorrectiveAction,
    revision: ExternallySuppliedRevision,
    parent: SpecificationVersion,
    identity: ApplicationIdentityContext,
) -> ActionApplication:
    """Materialize one caller-identified immutable child from supplied text."""

    if not isinstance(action, CorrectiveAction):
        raise TypeError("action must be a CorrectiveAction")
    if not isinstance(revision, ExternallySuppliedRevision):
        raise TypeError("revision must be an ExternallySuppliedRevision")
    if not isinstance(parent, SpecificationVersion):
        raise TypeError("parent must be a SpecificationVersion")
    if not isinstance(identity, ApplicationIdentityContext):
        raise TypeError("identity must be an ApplicationIdentityContext")
    if action.status is not CorrectiveActionStatus.PROPOSED:
        raise ValueError("only a PROPOSED action may be applied")
    if revision.action_ref != action.ref:
        raise ValueError("revision references the wrong action")
    if action.target_artifact_ref != parent.artifact_ref:
        raise ValueError("action targets the wrong parent artifact")
    if revision.parent_artifact_ref != parent.artifact_ref:
        raise ValueError("revision references the wrong parent artifact")
    child_ref = revision.requested_child_artifact_ref
    if (
        child_ref.artifact_id != parent.artifact_ref.artifact_id
        or child_ref.artifact_version == parent.artifact_ref.artifact_version
    ):
        raise ValueError("child must retain artifact identity and use a distinct version")
    if identity.applied_action_record_version == action.action_record_version:
        raise ValueError("APPLIED action record version must be caller-supplied and distinct")

    target_by_lineage = {item.lineage_id: item for item in action.target_requirements}
    parent_by_lineage = {item.lineage_id: item for item in parent.requirements}
    if tuple(parent_by_lineage) != tuple(item.lineage_id for item in parent.requirements):
        raise ValueError("parent lineages are not unique")
    replacements = {item.lineage_id: item for item in revision.replacements}
    if any(
        parent_by_lineage.get(lineage) is None
        or parent_by_lineage[lineage].subject_ref != target.subject_ref
        for lineage, target in target_by_lineage.items()
    ):
        raise ValueError("every action target must resolve to its exact parent subject")
    if not set(replacements).issubset(target_by_lineage):
        raise ValueError("revision may replace only action-target lineages")
    for lineage, replacement in replacements.items():
        parent_requirement = parent_by_lineage.get(lineage)
        if parent_requirement is None:
            raise ValueError("replacement lineage is absent from the parent")
        if replacement.expected_parent_subject_ref != parent_requirement.subject_ref:
            raise ValueError("replacement expected subject does not match the parent")
        if target_by_lineage[lineage].subject_ref != parent_requirement.subject_ref:
            raise ValueError("action target does not match the parent subject")

    application_id = ActionApplicationId(
        identity.application_instance_id,
        action.ref,
        revision.ref,
        child_ref,
    )
    application_ref = ActionApplicationRef(application_id, identity.application_version)
    action_after = replace(
        action,
        action_record_version=identity.applied_action_record_version,
        predecessor_action_ref=action.ref,
        status=CorrectiveActionStatus.APPLIED,
        external_revision_ref=revision.ref,
        application_ref=application_ref,
    )

    child_requirements = tuple(
        VersionedRequirement(
            item.lineage_id,
            RequirementSubjectRef(
                child_ref,
                item.subject_ref.requirement_id,
                item.subject_ref.source_line,
            ),
            replacements[item.lineage_id].replacement_text
            if item.lineage_id in replacements
            else item.text,
            item.subject_ref,
        )
        for item in parent.requirements
    )
    child_by_lineage = {item.lineage_id: item for item in child_requirements}
    changed_subjects = tuple(
        ChangedRequirementSubject(
            target.lineage_id,
            target.subject_ref,
            child_by_lineage[target.lineage_id].subject_ref,
        )
        for target in action.target_requirements
        if target.lineage_id in replacements
    )
    specification_provenance = SpecificationVersionProvenance(
        child_ref,
        parent.artifact_ref,
        application_ref,
        revision.ref,
        application_rule_ref_or_none=APPLICATION_RULE_REF,
    )
    child = SpecificationVersion(
        child_ref,
        parent.artifact_ref,
        application_ref,
        child_requirements,
        changed_subjects,
        specification_provenance,
    )
    transition_provenance = ArtifactTransitionProvenance(
        action.ref,
        action_after.ref,
        application_ref,
        revision.ref,
    )
    transition = ArtifactTransition(
        ArtifactTransitionId(identity.transition_instance_id, application_ref),
        parent.artifact_ref,
        child_ref,
        application_ref,
        revision.ref,
        changed_subjects,
        transition_provenance,
    )
    provenance = ActionApplicationProvenance(
        action.ref,
        action_after.ref,
        revision.ref,
        revision.provider_ref,
        parent.artifact_ref,
        child_ref,
    )
    return ActionApplication(
        application_id,
        identity.application_version,
        action.ref,
        action_after.ref,
        revision.ref,
        parent.artifact_ref,
        child_ref,
        changed_subjects,
        APPLICATION_RULE_REF,
        FullModelStatus.AVAILABLE,
        (ActionApplicationReason.EXTERNAL_REVISION_MATERIALIZED,),
        provenance,
        action_after,
        child,
        transition,
    )


__all__ = [
    "APPLICATION_RULE_REF",
    "ActionApplication",
    "ActionApplicationProvenance",
    "ActionApplicationReason",
    "ApplicationIdentityContext",
    "ArtifactTransition",
    "ArtifactTransitionId",
    "ArtifactTransitionProvenance",
    "ChangedRequirementSubject",
    "ExternalProviderRef",
    "ExternalRevisionProvenance",
    "ExternalRevisionProviderKind",
    "ExternallySuppliedRevision",
    "RequirementChangeKind",
    "RequirementTextReplacement",
    "SpecificationVersion",
    "SpecificationVersionProvenance",
    "VersionedRequirement",
    "apply_external_revision",
    "create_initial_specification_version",
]
