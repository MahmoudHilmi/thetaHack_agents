# ORACLE API Endpoints

## Base URL

```text
http://localhost:8000
```

Interactive API documentation is available at:

```text
http://localhost:8000/docs
```

## Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "api_configured": true,
  "graph_ready": true,
  "memory_ready": true
}
```

## Create a Decision

```http
POST /decide
Content-Type: application/json
```

Request body:

```json
{
  "problem_description": "هل يجب بناء مركز مجتمعي جديد في الحي؟",
  "user_input": "خذ التأثير البيئي والتكلفة في الاعتبار",
  "memory_scope": "district-cairo-01"
}
```

Request fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `problem_description` | string | Yes | The decision problem to analyze. |
| `user_input` | string | No | Extra context for the expert agents. Defaults to an empty string. |
| `memory_scope` | string | No | Isolates decision memory for a user, district, or organization. Defaults to `default`. |

Success response (`200`):

```json
{
  "final_decision": "Approve with conditions",
  "decision_reasoning": "The social and economic benefits are strong when environmental safeguards are applied.",
  "final_confidence": 0.82,
  "climate_analysis": "...",
  "economy_analysis": "...",
  "health_analysis": "...",
  "citizen_perspective": "...",
  "ethics_evaluation": "...",
  "memory_matches": 1,
  "status": "success"
}
```

Response fields:

| Field | Type | Description |
| --- | --- | --- |
| `final_decision` | string | Final recommendation from the Judge Agent. |
| `decision_reasoning` | string | Explanation for the recommendation. |
| `final_confidence` | number | Confidence score from 0 to 1. |
| `climate_analysis` | string | Climate-agent analysis. |
| `economy_analysis` | string | Economy-agent analysis. |
| `health_analysis` | string | Health-agent analysis. |
| `citizen_perspective` | string | Citizen-agent analysis. |
| `ethics_evaluation` | string | Ethics-agent analysis. |
| `memory_matches` | integer | Number of relevant prior decisions included as context. |
| `status` | string | Request status. |

## Error Responses

| Status | Meaning |
| --- | --- |
| `422` | Invalid request body, for example a missing `problem_description`. |
| `503` | The LLM provider is not configured or the graph is unavailable. |
| `500` | The decision workflow failed. |

## cURL Example

```bash
curl -X POST http://localhost:8000/decide \
  -H "Content-Type: application/json" \
  -d '{
    "problem_description": "Should a new community center be built?",
    "user_input": "Consider environmental and cost impacts.",
    "memory_scope": "district-cairo-01"
  }'
```
