from robyn import SubRouter, Response


tasks_route = SubRouter(__file__, prefix="/tasks")


@tasks_route.get("/")
async def get_tasks():
    return Response(status_code=200, json={"message": "Hello, World!"})
