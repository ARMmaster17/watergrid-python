from watergrid.middleware.PipelineMiddlware import PipelineMiddleware
from watergrid.pipelines.pipeline_verifier import PipelineVerifier


class StepOrderingMiddleware(PipelineMiddleware):
    def pre_pipeline(self, pipeline):
        PipelineVerifier.verify_pipeline_dependencies_fulfilled(
            pipeline._steps
        )
        PipelineVerifier.verify_pipeline_step_ordering(pipeline._steps)

    def post_pipeline(self, pipeline):
        pass

    def __init__(self):
        super().__init__()
