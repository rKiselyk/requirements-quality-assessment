"""Read-only USER and AUDIT projections for the completed Full Model v0.1 path.

The reporters in this module only select and format fields from already-computed
typed records.  They do not detect evidence, assess a characteristic, aggregate
values, compare results, classify risk, or choose an action.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, fields, is_dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from pathlib import Path

from .corrective_action import (
    ActionApplication,
    CorrectiveAction,
    CorrectiveActionResolution,
    ExternallySuppliedRevision,
    SpecificationVersion,
)
from .cross_analysis import SpecificationAssessmentResult
from .defect_quality import (
    DefectPopulationSnapshot,
    DefectQualityRelation,
    ProblemClaimResolution,
)
from .dynamic_evidence import (
    ConformanceAssessment,
    CriterionBindingResult,
    ObservationResolution,
)
from .metrics import ArtifactRef, MetricProfile
from .performance_efficiency import PerformanceEfficiencyFeatureProfile
from .process import ProcessAssessmentState, ProcessStateTransition
from .product_quality import ProductQualityAssessment
from .product_quality_prediction import PredictedPerformanceEfficiency
from .reassessment import (
    CoreReassessmentResults,
    FullModelDownstreamRecords,
    ReassessmentRun,
    ResultComparison,
)
from .risk import BoundedRiskAssessment


@dataclass(frozen=True, slots=True)
class FullModelReportBundle:
    """Completed records available to one Full Model v0.1 report.

    The base specification assessment is required so requirement C/V/U,
    specification aggregates, and QB-v0.1 remain the same records used by the
    existing reporters.  Every downstream record is optional because the
    approved model represents unavailable, unresolved, unsupported, and
    not-applicable paths explicitly.
    """

    assessment_result: SpecificationAssessmentResult
    metric_profile: MetricProfile | None = None
    criterion_binding: CriterionBindingResult | None = None
    observation_resolution: ObservationResolution | None = None
    conformance: ConformanceAssessment | None = None
    feature_profile: PerformanceEfficiencyFeatureProfile | None = None
    product_quality_assessment: ProductQualityAssessment | None = None
    predicted_product_quality: PredictedPerformanceEfficiency | None = None
    problem_resolutions: tuple[ProblemClaimResolution, ...] = ()
    defect_population: DefectPopulationSnapshot | None = None
    defect_quality_relations: tuple[DefectQualityRelation, ...] = ()
    risk_assessments: tuple[BoundedRiskAssessment, ...] = ()
    corrective_action_resolutions: tuple[CorrectiveActionResolution, ...] = ()
    corrective_actions: tuple[CorrectiveAction, ...] = ()
    specification_versions: tuple[SpecificationVersion, ...] = ()
    external_revisions: tuple[ExternallySuppliedRevision, ...] = ()
    action_applications: tuple[ActionApplication, ...] = ()
    reassessment_runs: tuple[ReassessmentRun, ...] = ()
    comparisons: tuple[ResultComparison, ...] = ()
    process_states: tuple[ProcessAssessmentState, ...] = ()
    process_transitions: tuple[ProcessStateTransition, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.assessment_result, SpecificationAssessmentResult):
            raise TypeError(
                "assessment_result must be a SpecificationAssessmentResult"
            )
        optional_fields = (
            ("metric_profile", self.metric_profile, MetricProfile),
            ("criterion_binding", self.criterion_binding, CriterionBindingResult),
            (
                "observation_resolution",
                self.observation_resolution,
                ObservationResolution,
            ),
            ("conformance", self.conformance, ConformanceAssessment),
            (
                "feature_profile",
                self.feature_profile,
                PerformanceEfficiencyFeatureProfile,
            ),
            (
                "product_quality_assessment",
                self.product_quality_assessment,
                ProductQualityAssessment,
            ),
            (
                "predicted_product_quality",
                self.predicted_product_quality,
                PredictedPerformanceEfficiency,
            ),
            (
                "defect_population",
                self.defect_population,
                DefectPopulationSnapshot,
            ),
        )
        for name, value, expected_type in optional_fields:
            if value is not None and not isinstance(value, expected_type):
                raise TypeError(f"{name} must be a {expected_type.__name__} record")
        tuple_fields = (
            ("problem_resolutions", self.problem_resolutions, ProblemClaimResolution),
            (
                "defect_quality_relations",
                self.defect_quality_relations,
                DefectQualityRelation,
            ),
            ("risk_assessments", self.risk_assessments, BoundedRiskAssessment),
            (
                "corrective_action_resolutions",
                self.corrective_action_resolutions,
                CorrectiveActionResolution,
            ),
            ("corrective_actions", self.corrective_actions, CorrectiveAction),
            (
                "specification_versions",
                self.specification_versions,
                SpecificationVersion,
            ),
            (
                "external_revisions",
                self.external_revisions,
                ExternallySuppliedRevision,
            ),
            ("action_applications", self.action_applications, ActionApplication),
            ("reassessment_runs", self.reassessment_runs, ReassessmentRun),
            ("comparisons", self.comparisons, ResultComparison),
            ("process_states", self.process_states, ProcessAssessmentState),
            (
                "process_transitions",
                self.process_transitions,
                ProcessStateTransition,
            ),
        )
        for name, values, expected_type in tuple_fields:
            if not isinstance(values, tuple) or any(
                not isinstance(item, expected_type) for item in values
            ):
                raise TypeError(f"{name} must contain {expected_type.__name__} records")


def _fraction(value: Fraction) -> str:
    return f"Fraction({value.numerator},{value.denominator})"


def _decimal(value: Decimal) -> str:
    return f"Decimal('{value}')"


def _scalar(value: object) -> str:
    if value is None:
        return "NONE"
    if isinstance(value, Enum):
        return str(value.value)
    if type(value) is Fraction:
        return _fraction(value)
    if type(value) is Decimal:
        return _decimal(value)
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (str, int)):
        return str(value)
    return repr(value)


def _audit_node(label: str, value: object, indent: int = 0) -> list[str]:
    prefix = " " * indent
    if is_dataclass(value) and not isinstance(value, type):
        lines = [f"{prefix}{label}: {type(value).__name__}"]
        for item in fields(value):
            lines.extend(_audit_node(item.name, getattr(value, item.name), indent + 2))
        return lines
    if isinstance(value, tuple):
        lines = [f"{prefix}{label}:"]
        if not value:
            lines.append(f"{prefix}  []")
            return lines
        for index, item in enumerate(value):
            lines.extend(_audit_node(f"[{index}]", item, indent + 2))
        return lines
    if isinstance(value, Mapping):
        lines = [f"{prefix}{label}:"]
        if not value:
            lines.append(f"{prefix}  {{}}")
            return lines
        for key in sorted(value, key=lambda item: _scalar(item)):
            lines.extend(_audit_node(_scalar(key), value[key], indent + 2))
        return lines
    if isinstance(value, (list, set, frozenset)):
        ordered = tuple(value) if isinstance(value, list) else tuple(
            sorted(value, key=_scalar)
        )
        return _audit_node(label, ordered, indent)
    return [f"{prefix}{label}: {_scalar(value)}"]


_AUDIT_RECORDS = (
    ("metric_profile", "Metric profile"),
    ("criterion_binding", "Dynamic criterion binding"),
    ("observation_resolution", "Dynamic observation"),
    ("conformance", "Criterion conformance"),
    ("feature_profile", "X_PE feature profile"),
    ("product_quality_assessment", "Bounded Performance Efficiency assessment"),
    ("predicted_product_quality", "Predicted product quality (y_hat_PE)"),
    ("problem_resolutions", "Problem claim resolutions"),
    ("defect_population", "Defect population"),
    ("defect_quality_relations", "R_DQ relations"),
    ("risk_assessments", "Bounded risk assessments"),
    ("corrective_action_resolutions", "Corrective action resolutions"),
    ("corrective_actions", "Corrective actions"),
    ("specification_versions", "Specification versions"),
    ("external_revisions", "External revisions"),
    ("action_applications", "Action applications"),
    ("reassessment_runs", "Reassessments"),
    ("comparisons", "Before/after comparisons"),
    ("process_states", "Process assessment states"),
    ("process_transitions", "Process state transitions"),
)


class AuditFullModelReporter:
    """Render the existing audit view plus exact Full Model record fields."""

    def render(self, bundle: FullModelReportBundle) -> str:
        if not isinstance(bundle, FullModelReportBundle):
            raise TypeError("audit full-model view requires FullModelReportBundle")
        from .reporter import ConsoleReporter

        base = ConsoleReporter().render_assessment(bundle.assessment_result)
        return f"{base}\n\n{self.render_projection(bundle)}"

    def render_projection(self, bundle: FullModelReportBundle) -> str:
        sections = ["Full Model v0.1 audit path"]
        for attribute, heading in _AUDIT_RECORDS:
            value = getattr(bundle, attribute)
            if value is None or value == ():
                continue
            sections.append("\n".join(_audit_node(heading, value)))
        return "\n\n".join(sections)


def _user_exact(value: object) -> str:
    if value is None:
        return "NONE"
    if isinstance(value, Enum):
        return str(value.value)
    if type(value) is Fraction:
        return f"{value.numerator}/{value.denominator}"
    if type(value) is Decimal:
        return str(value)
    return str(value)


def _artifact_ref(bundle: FullModelReportBundle) -> ArtifactRef | None:
    if bundle.metric_profile is not None:
        return bundle.metric_profile.artifact_ref
    if bundle.feature_profile is not None:
        return bundle.feature_profile.artifact_ref
    if bundle.process_states:
        return bundle.process_states[0].artifact_ref
    return None


def _state_value(value: object) -> str:
    status = _user_exact(value.status)
    applicability = _user_exact(value.applicability)
    exact = getattr(value, "exact_value", None)
    categorical = getattr(value, "categorical_state", None)
    if exact is not None:
        rendered = _user_exact(exact)
    elif categorical is not None:
        rendered = _user_exact(categorical)
    else:
        rendered = status
    return f"{rendered} (status={status}; applicability={applicability})"


class UserFullModelReporter:
    """Render a concise interpretation without changing typed model meanings."""

    def render(self, bundle: FullModelReportBundle) -> str:
        if not isinstance(bundle, FullModelReportBundle):
            raise TypeError("user full-model view requires FullModelReportBundle")
        from .reporter import UserConsoleReporter

        base = UserConsoleReporter().render_assessment(bundle.assessment_result)
        return f"{base}\n\n{self.render_projection(bundle)}"

    def render_projection(self, bundle: FullModelReportBundle) -> str:
        sections = ["Повна модель v0.1"]
        context = self._context(bundle)
        if context:
            sections.append("\n".join(("Контекст артефакту і процесу", *context)))
        sections.append(self._requirement_and_specification_quality(bundle))

        dynamic = self._dynamic_and_product_quality(bundle)
        if dynamic:
            sections.append("\n".join(("Спостережуваний показник якості продукту", *dynamic)))

        predicted = self._predicted_product_quality(bundle)
        if predicted:
            sections.append("\n".join(("Прогнозована якість продукту (ŷ_PE)", *predicted)))

        defect = self._defect_and_risk(bundle)
        if defect:
            sections.append("\n".join(("Проблема, R_DQ і обмежений ризик", *defect)))

        action = self._action_and_revision(bundle)
        if action:
            sections.append("\n".join(("Коригувальна дія і зовнішня ревізія", *action)))

        reassessment = self._reassessment_and_comparison(bundle)
        if reassessment:
            sections.append("\n".join(("Переоцінювання і порівняння", *reassessment)))

        process = self._process(bundle)
        if process:
            sections.append("\n".join(("Перехід стану процесу", *process)))

        sections.append(self._limitations())
        return "\n\n".join(sections)

    @staticmethod
    def _context(bundle: FullModelReportBundle) -> list[str]:
        lines: list[str] = []
        artifact = _artifact_ref(bundle)
        if artifact is not None:
            lines.append(
                f"Артефакт: {artifact.artifact_id}; версія: {artifact.artifact_version}"
            )
        if bundle.metric_profile is not None:
            assessment = bundle.metric_profile.assessment_ref
            lines.append(
                f"Оцінювання: {assessment.assessment_id}; версія: "
                f"{assessment.assessment_version}"
            )
        for state in bundle.process_states:
            lines.append(
                f"Стан процесу: {state.process_state_id} / "
                f"{state.process_state_version}; stage={state.stage.value}"
            )
        return lines

    @staticmethod
    def _predicted_product_quality(bundle: FullModelReportBundle) -> list[str]:
        prediction = bundle.predicted_product_quality
        if prediction is None:
            return []
        value = (
            _user_exact(prediction.predicted_value)
            if prediction.predicted_value is not None
            else prediction.status.value
        )
        parameter_identity = prediction.parameter_set_ref.identity
        return [
            "Прогноз Performance Efficiency: "
            f"{value} (kind={prediction.result_kind.value}; "
            f"status={prediction.status.value}; "
            f"applicability={prediction.applicability.value})",
            "F_θ,PE: "
            f"{prediction.predictor_ref.predictor_id} / "
            f"{prediction.predictor_ref.predictor_version}; θ="
            f"{parameter_identity.parameter_set_id} / "
            f"{parameter_identity.parameter_set_version}; "
            f"calibration={prediction.calibration_status.value}",
            "Це прогнозований результат, а не спостережуваний індикатор; "
            "оцінка впевненості, невизначеність і прогнозна валідність не заявляються.",
        ]

    @staticmethod
    def _requirement_and_specification_quality(
        bundle: FullModelReportBundle,
    ) -> str:
        qb = bundle.assessment_result.specification_assessment.qb_consistency
        value = _user_exact(qb.value) if qb.value is not None else qb.state.value
        return "\n".join(
            (
                "Якість вимог і специфікації",
                "C/V/U вище є профілем якості вимог; це не показник якості продукту.",
                "Агрегати C/V/U вище є окремими властивостями специфікації.",
                f"QB consistency: {value} (state={qb.state.value}; bounded=QB-v0.1)",
            )
        )

    @staticmethod
    def _dynamic_and_product_quality(bundle: FullModelReportBundle) -> list[str]:
        lines: list[str] = []
        binding = bundle.criterion_binding
        if binding is not None:
            lines.append(
                "Критерій: "
                f"status={binding.status.value}; applicability={binding.applicability.value}"
            )
            if binding.criterion is not None:
                criterion = binding.criterion
                lines.append(
                    "Межа критерію: "
                    f"{criterion.comparator.value} {_user_exact(criterion.bound)} "
                    f"{criterion.unit.value}"
                )
        resolution = bundle.observation_resolution
        if resolution is not None:
            lines.append(
                "Спостереження: "
                f"status={resolution.status.value}; "
                f"applicability={resolution.applicability.value}"
            )
            if resolution.observation is not None:
                observation = resolution.observation
                lines.append(
                    "Спостережене значення: "
                    f"{_user_exact(observation.observed_value)} {observation.unit.value}"
                )
        conformance = bundle.conformance
        if conformance is not None:
            outcome = (
                conformance.outcome.value
                if conformance.outcome is not None
                else conformance.status.value
            )
            lines.append(
                "Відповідність критерію: "
                f"{outcome} (status={conformance.status.value}; "
                f"applicability={conformance.applicability.value})"
            )
        profile = bundle.feature_profile
        if profile is not None:
            lines.append(
                f"X_PE: status={profile.status.value}; "
                f"applicability={profile.applicability.value}"
            )
            lines.extend(
                f"  {feature.feature_id.value}: {feature.status.value} / "
                f"{feature.applicability.value}"
                for feature in profile.features
            )
        quality = bundle.product_quality_assessment
        if quality is not None:
            value = (
                _user_exact(quality.value)
                if quality.value is not None
                else quality.status.value
            )
            lines.append(
                "Обмежена оцінка Performance Efficiency: "
                f"{value} (kind={quality.result_kind.value}; "
                f"status={quality.status.value}; applicability={quality.applicability.value})"
            )
            lines.append(
                "Це спостережуваний індикатор одного критерію часу відгуку, "
                "а не повне оцінювання Performance Efficiency."
            )
        return lines

    @staticmethod
    def _defect_and_risk(bundle: FullModelReportBundle) -> list[str]:
        lines: list[str] = []
        for resolution in bundle.problem_resolutions:
            problem = resolution.problem
            problem_text = (
                f"{problem.problem_kind.value}; id={problem.problem_id}"
                if problem is not None
                else "відсутній у цьому bounded result"
            )
            lines.append(
                "Підтверджена підтримувана проблема: "
                f"{problem_text} (status={resolution.status.value}; "
                f"applicability={resolution.applicability.value}; "
                f"disposition={resolution.disposition.value})"
            )
        if bundle.defect_population is not None:
            population = bundle.defect_population
            lines.append(
                "D_v0.1: "
                f"status={population.status.value}; "
                f"applicability={population.applicability.value}; "
                f"population_complete={str(population.population_complete).lower()}"
            )
        for relation in bundle.defect_quality_relations:
            lines.append(
                "R_DQ: "
                f"{relation.relation_kind.value} (status={relation.status.value}; "
                f"applicability={relation.applicability.value}; "
                f"characteristic={relation.characteristic_id.value})"
            )
        for risk in bundle.risk_assessments:
            classification = (
                risk.classification.value
                if risk.classification is not None
                else risk.status.value
            )
            lines.append(
                "Обмежений ризик: "
                f"{classification} (status={risk.status.value}; "
                f"applicability={risk.applicability.value}; "
                f"calibration={risk.calibration_status.value})"
            )
        if bundle.problem_resolutions or bundle.defect_population is not None:
            lines.append(
                "Відсутність підтвердженої проблеми в D_v0.1 не означає "
                "відсутність дефектів."
            )
        return lines

    @staticmethod
    def _action_and_revision(bundle: FullModelReportBundle) -> list[str]:
        lines: list[str] = []
        actions = [
            resolution.action
            for resolution in bundle.corrective_action_resolutions
            if resolution.action is not None
        ]
        actions.extend(bundle.corrective_actions)
        for action in actions:
            lines.append(
                "Коригувальна дія: "
                f"{action.action_kind.value}; status={action.status.value}; "
                f"record_version={action.action_record_version}"
            )
        for revision in bundle.external_revisions:
            lines.append(
                "Зовнішня ревізія: "
                f"{revision.revision_id} / {revision.revision_version}; "
                f"provider={revision.provider_kind.value}; "
                f"child={revision.requested_child_artifact_ref.artifact_version}"
            )
        for application in bundle.action_applications:
            lines.append(
                "Застосування: "
                f"status={application.status.value}; "
                f"{application.parent_artifact_ref.artifact_version} → "
                f"{application.child_artifact_ref.artifact_version}"
            )
        if actions or bundle.action_applications:
            lines.append(
                "Пропозиція, застосування або зміна стану не доводять "
                "результативність коригувальної дії."
            )
        return lines

    @staticmethod
    def _reassessment_and_comparison(bundle: FullModelReportBundle) -> list[str]:
        lines: list[str] = []
        for run in bundle.reassessment_runs:
            child = (
                f"{run.context.child_artifact_ref.artifact_id} / "
                f"{run.context.child_artifact_ref.artifact_version}"
            )
            lines.append(
                f"ReEval: {run.reassessment_id} / {run.reassessment_version}; "
                f"status={run.status.value}; child={child}"
            )
            for result in run.produced_results:
                if isinstance(result, CoreReassessmentResults):
                    lines.extend(UserFullModelReporter._child_core(result))
                elif isinstance(result, FullModelDownstreamRecords):
                    lines.extend(UserFullModelReporter._child_downstream(result))
        for comparison in bundle.comparisons:
            subject = comparison.comparison_subject
            subject_text = (
                f"{subject.result_family.value}:{subject.metric_or_characteristic_id}"
                if subject is not None
                else "UNRESOLVED_SUBJECT"
            )
            kind = (
                comparison.comparison_kind.value
                if comparison.comparison_kind is not None
                else comparison.status.value
            )
            if (
                comparison.before_state_and_value is not None
                and comparison.after_state_and_value is not None
            ):
                values = (
                    f"{_state_value(comparison.before_state_and_value)} → "
                    f"{_state_value(comparison.after_state_and_value)}"
                )
            else:
                values = "before/after unavailable"
            reasons = ", ".join(item.value for item in comparison.reason_codes)
            lines.append(
                f"{subject_text}: {values}; comparison={kind}; reasons={reasons}"
            )
        if bundle.comparisons:
            lines.append(
                "INCREASED і DECREASED є лише напрямами точного порівняння; "
                "STATE_CHANGED є лише структурованою зміною."
            )
            lines.append(
                "Порівняння не встановлює причинний ефект або результативність дії."
            )
        return lines

    @staticmethod
    def _child_core(result: CoreReassessmentResults) -> list[str]:
        lines = [
            "S(v2) — якість вимог (C/V/U, окремо від якості продукту):"
        ]
        for record in result.requirement_records:
            profile = record.quality_profile
            values = []
            for label, assessment in (
                ("C", profile.completeness),
                ("V", profile.verifiability),
                ("U", profile.unambiguity),
            ):
                value = (
                    _user_exact(assessment.value)
                    if assessment.value is not None
                    else assessment.state.value
                )
                values.append(f"{label}={value}")
            requirement_id = record.extraction_result.requirement.id
            lines.append(f"  {requirement_id}: {'; '.join(values)}")
        specification = result.specification_assessment.specification_assessment
        quality = specification.quality_profile
        aggregates = []
        for label, aggregate in (
            ("C", quality.completeness),
            ("V", quality.verifiability),
            ("U", quality.unambiguity),
        ):
            value = (
                _user_exact(aggregate.value)
                if aggregate.value is not None
                else aggregate.state.value
            )
            aggregates.append(f"{label}={value}")
        lines.append(f"S(v2) — агрегати специфікації: {'; '.join(aggregates)}")
        qb = specification.qb_consistency
        qb_value = _user_exact(qb.value) if qb.value is not None else qb.state.value
        lines.append(
            f"S(v2) — QB consistency: {qb_value} (state={qb.state.value})"
        )
        return lines

    @staticmethod
    def _child_downstream(result: FullModelDownstreamRecords) -> list[str]:
        quality = result.product_quality_assessment
        quality_value = (
            _user_exact(quality.value)
            if quality.value is not None
            else quality.status.value
        )
        problem = result.target_problem_resolution.problem
        problem_state = (
            problem.problem_kind.value
            if problem is not None
            else result.target_problem_resolution.status.value
        )
        risk = result.risk_assessment
        risk_state = (
            risk.classification.value
            if risk.classification is not None
            else risk.status.value
        )
        return [
            "S(v2) — dynamic/conformance: "
            f"{result.conformance.status.value} / "
            f"{_user_exact(result.conformance.outcome)}",
            "S(v2) — X_PE: "
            f"{result.feature_profile.status.value} / "
            f"{result.feature_profile.applicability.value}",
            "S(v2) — bounded PE indicator: "
            f"{quality_value} (status={quality.status.value})",
            f"S(v2) — confirmed problem: {problem_state}",
            "S(v2) — R_DQ: "
            f"{result.defect_quality_relation.status.value} / "
            f"{result.defect_quality_relation.applicability.value}",
            f"S(v2) — bounded risk: {risk_state}",
        ]

    @staticmethod
    def _process(bundle: FullModelReportBundle) -> list[str]:
        lines: list[str] = []
        for transition in bundle.process_transitions:
            before = transition.predecessor_process_state_ref
            after = transition.successor_process_state_ref
            lines.append(
                f"{before.process_state_id} / {before.process_state_version} → "
                f"{after.process_state_id} / {after.process_state_version}; "
                f"stage={after.stage.value}"
            )
        return lines

    @staticmethod
    def _limitations() -> str:
        return "\n".join(
            (
                "Важливі межі",
                "- RISK_IDENTIFIED означає лише визначену bounded presence; "
                "величина ризику не обчислюється.",
                "- NOT_APPLICABLE не є твердженням про безпечність.",
                "- Відсутність підтвердженої проблеми не означає відсутність дефектів.",
                "- Спостережуваний PE indicator не є повною Performance Efficiency.",
                "- Зміна стану або різниця переоцінювання не є причинним висновком.",
            )
        )


# Symmetric aliases make both common adjective orders discoverable.
FullModelAuditReporter = AuditFullModelReporter
FullModelUserReporter = UserFullModelReporter


__all__ = [
    "AuditFullModelReporter",
    "FullModelAuditReporter",
    "FullModelReportBundle",
    "FullModelUserReporter",
    "UserFullModelReporter",
]
