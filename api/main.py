# api/main.py
from flask import Flask, jsonify, request
from temporalio.client import Client
from uuid import uuid4


app = Flask(__name__)

temporal_client = Client(target="temporal:7233")

@app.route("/request", methods=["POST"])
async def create_request():
    request_id = str(uuid4())
    # Start the temporal workflow
    await temporal_client.start_workflow(
        "ProcessRequestWorkflow",
        id=f"request-{request_id}",
        task_queue="request-queue",
        arg=request.get_json()
    )
    
    return jsonify({
        "request_id": request_id,
        "callback_url": f"/request/{request_id}/status"
    })


@app.route("/request/<request_id>/status", methods=["GET"])
async def get_status(request_id):
    # Get workflow handle
    handle = await temporal_client.get_workflow_handle(f"request-{request_id}")
    try:
        # Query workflow status
        status = await handle.query("get_status")
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


"""
    def post_appcode_onboard(self, appcode: str, headers: dict = None):
        # basic validation of parameters
        if appcode is None:
            return self._render_response("", "", "Must provide App Code"), 400

        try:
            _AppcodeRequest = AppcodeOnboardRequestSchema().load(request.get_json())  # parse incoming request
        except MarshmallowError as e:
            message = "Failed to deserialize request body."
            self.LOG.exception(message)
            return self._render_response(None, None, "MarshmallowError: " + e.args[0]), 400
        except TypeError as e:
            message = "TypeError: Failed to deserialize request body."
            self.LOG.exception(message)
            return self._render_response(None, None, "TypeError: " + e.args[0]), 400
        
        _workflow_config = config.temporal_workflow_config.get_workflow_config("appcode_onboard")
        if _workflow_config is None:
            return self._render_response("", "", "Failed to get workflow config"), 400

        # set all necessary parameters
        _appcode = appcode.lower()
        _service_tier = _AppcodeRequest.service_tier.lower()
        _workflow_request_object = AppCode(appcode=_appcode, request=_AppcodeRequest, id=None)
        _solution_id = str(_AppcodeRequest.solutions[0]).lower()  # get solution ID
        _workflow_id = f"{appcode.upper()}::{_service_tier.upper()}::AppCodeOnboard"

        # submit temporal request to async execute workflow described by _workflow_config
        # try:
        future = self._executor.submit(
            asyncio.run,
            start_temporal_workflow_execution(
                appcode=_appcode,
                service_tier=_service_tier,
                workflow_payload_request=_workflow_request_object,
                headers=headers,
            )
        )
        _wf_result = future.result()
        self.LOG.info(f"Spawned workflow with workflow ID {_workflow_id}, intermediate workflow result: {_wf_result}")
        return self._render_response(_appcode, _solution_id), 201
"""

