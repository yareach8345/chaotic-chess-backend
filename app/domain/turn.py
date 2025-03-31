import abc
from enum import Enum
from typing import Self

from app.domain.chess_game import ChessGame
from app.dto.move_dto import MoveDto, PieceColor
from app.exception.game_exception import GameException


class MoveResult(Enum):
    ONGOING = "ongoing"
    CHECKMATE_USER_WIN = "checkmate_user_win"
    CHECKMATE_USER_LOSE = "checkmate_user_lose"
    USER_LOSE_CUZ_KILL_KING = "user_lose_cuz_kill_king"
    ILLEGAL_INPUT = "illegal_input"

class Turn(metaclass=abc.ABCMeta):
    _color: bool
    _game: ChessGame

    #color : 유저 혹은 ai의 색을 나타냄, True = 백, False = 흑
    def __init__(self, color: bool, game: ChessGame):
        self._game = game
        self._color = color

    def _check(self, move_dto: MoveDto):
        if self._color != self._game.turn:
            raise GameException(f"It's not turn. but try move")

        if self._color != (move_dto.color == PieceColor.WHITE):
            raise GameException(f"It's is trying move users piece!")

    def _before_moving(self, move_dto: MoveDto) -> MoveResult:
        pass

    def _moving(self, move_dto: MoveDto) -> MoveResult:
        pass

    def _after_turn(self, move_dto: MoveDto) -> MoveResult:
        self._game.after_turn(move_dto.to_algebraic())
        return MoveResult.ONGOING

    def _after_moving(self, move_dto: MoveDto) -> MoveResult:
        pass

    def _generate_next_turn(self) -> Self:
        pass

    def move(self, move_dto: MoveDto) -> Self | MoveResult:
        chain = [
            self._before_moving,
            self._moving,
            self._after_turn,
            self._after_moving
        ]

        self._check(move_dto)

        for step in chain:
            result = step(move_dto)
            if result is not MoveResult.ONGOING:
                return result

        return self._generate_next_turn()

def generate_turn(game: ChessGame) -> Turn:
    from app.domain.user_turn import UserTurn
    from app.domain.ai_turn import AITurn
    if game.turn == game.user_color:
        return UserTurn(game)
    else:
        return AITurn(game)


