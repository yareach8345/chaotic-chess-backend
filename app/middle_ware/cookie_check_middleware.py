from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.container import container
from app.repositories.chess_repository import ChessRepository


class CookieCheckMiddleware(BaseHTTPMiddleware):
    _repository: ChessRepository = container.chess_repository()

    async def dispatch(self, request: Request, call_next):
        #해당 요청이 game init에 대한 요청이 아니며
        path = request.url.path
        if path.startswith("/api") and not((path.endswith("/game/") or path.endswith("/game")) and request.method == "POST"):
            game_id = request.cookies.get("game_id")
            #game_id라는 쿠키가 없을 시
            if game_id is None:
                #실패한다
                return JSONResponse(status_code=400, content={"message": "No cookie named 'game_id'"})
            #혹은 game_id를 id로 가진 데이터가 db에 없을 시
            if (await self._repository.get_by_id(game_id)) is None:
                #실패한다
                response = JSONResponse(status_code=400, content={"message": "No cookie named 'game_id' is expired"})
                #쿠키 삭제는 덤이다.
                response.delete_cookie("game_id")
                return response
        #아니면 진행
        response = await call_next(request)
        return response
