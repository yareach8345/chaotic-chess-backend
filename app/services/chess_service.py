from typing import List

from chess import Board
from pydantic import BaseModel

from app.domain.chess_game import ChessGame
from app.domain.turn import generate_turn, Turn, MoveResult
from app.dto.ai_request_dto import AIRequestDTO
from app.dto.db_update_dto import DBUpdateWithMovingDto
from app.dto.game_info_dto import GameInfoDTO, from_chess_game_schema
from app.dto.game_init_dto import GameInitDTO
from app.dto.move_dto import MoveDto
from app.dto.turn_result_dto import TurnResultDTO
from app.repositories.i_chess_repository import IChessRepository
from app.schemas.chess_game_schema import ChessGameSchema
from app.services.ai_service import AIService

from app.services.i_chess_service import IChessService
from app.utils.chess_util import init_game


class _TurnResult(BaseModel):
    moves: List[str]
    move_result: MoveResult
    ai_message: str | None


class ChessService(IChessService):
    _repository: IChessRepository
    _ai_service: AIService

    def __init__(self, repository: IChessRepository, ai_service: AIService):
        self._repository = repository
        self._ai_service = ai_service

    async def init_game(self, game_info_dto: GameInitDTO) -> GameInfoDTO:
        b = init_game()

        new_game_schema = ChessGameSchema(
            game_status="ongoing",
            white=game_info_dto.first,
            moves=[],
            current_fen=b.fen(),
        )

        new_game_id = await self._repository.save(new_game_schema)
        result = from_chess_game_schema(new_game_schema)
        result.game_id = new_game_id
        return result

    async def load_game(self, game_id: str) -> GameInfoDTO | None:
        schema = await self._repository.get_by_id(game_id)
        if schema is not None:
            return from_chess_game_schema(schema)
        else:
            return None

    async def _take_a_move(self, chess_game: ChessGame, user_move: MoveDto) -> _TurnResult:
        moves_in_this_turn = []
        #턴 객체를 생성
        user_turn = generate_turn(chess_game)
        #유저의 턴을 진행한다.
        user_turn_result = user_turn.move(user_move)

        moves_in_this_turn.append(user_move.moving)
        #만약 결과가 MoveResult이며, ONGOING이 아닐 경우 게임이 끝난 것이므로 종료한다.
        if isinstance(user_turn_result, MoveResult) and user_turn_result != MoveResult.ONGOING:
            return _TurnResult(
                moves = moves_in_this_turn,
                move_result = user_turn_result,
                ai_message = None
            )
        #턴객체라면 진행한다. 읽기 쉽게 변수명을 변경한다.
        elif isinstance(user_turn_result, Turn):
            ai_move = user_turn_result
        else:
            raise Exception("IMPASSIBLE")

        #반복문은 ai가 엉뚱한 답을 보냈을 경우 다시 실행하기 위함
        while(True):
            #ai의 움직임을 생성하고
            ai_moving = self._ai_service.get_next_move(
                AIRequestDTO(
                    moves=chess_game.moves,
                    user_move=user_move.to_uci(),
                    ai_role="white" if chess_game.ai_color == True else "black",
                    fen=chess_game.board.fen()
                )
            )
            ai_move_dto = MoveDto(moving=ai_moving.ai_moving)
            #파싱 가능한지 검사
            if ai_move_dto.can_parsing():
                # 턴을 진행한다.
                ai_turn_result = ai_move.move(ai_move_dto)

                moves_in_this_turn.append(ai_move_dto.moving)
                break
        if isinstance(ai_move_dto, MoveResult):
            return _TurnResult(
                moves = moves_in_this_turn,
                move_result= ai_turn_result,
                ai_message = ai_moving.message_to_user
            )
        else:
            return _TurnResult(
                moves = moves_in_this_turn,
                move_result= MoveResult.ONGOING,
                ai_message = ai_moving.message_to_user
            )


    async def take_a_turn(self, game_id: str, user_move: MoveDto) -> TurnResultDTO | MoveResult:
        chess_game = ChessGame(await self._repository.get_by_id(game_id))
        #턴을 진행하고
        turn_result = await self._take_a_move(chess_game, user_move)

        #게임이 계속될 수 있는지 확인한다. 만약 종료해야 하는 경우는
        if turn_result.move_result != MoveResult.ONGOING:
            #게임을 종료 처리 후
            await self._repository.end_game(game_id)

        #db에 저장한다.
        game_info_after_turn = GameInfoDTO(
            game_id = game_id,
            moves = chess_game.moves,
            white = "ai" if chess_game.ai_color == True else "user",
            fen = chess_game.board.fen(),
            game_status = "ongoing",
        )
        await self._repository.update_by_moving(game_id, DBUpdateWithMovingDto(
            moves = turn_result.moves,
            new_fen = game_info_after_turn.fen
        ))

        result = TurnResultDTO(
            game_info=game_info_after_turn,
            move_result=turn_result.move_result,
            moves_in_this_turn=turn_result.moves,
            ai_saying = turn_result.ai_message
        )
        return result

    async def get_history(self, game_id: str) -> List[str]:
        return (await self._repository.get_by_id(game_id)).moves

    async def end_game(self, game_id: str):
        await self._repository.end_game(game_id)

    async def reset_game(self, game_id: str) -> GameInfoDTO:
        await self._repository.reset_game(game_id)
        return from_chess_game_schema(await self._repository.get_by_id(game_id))
