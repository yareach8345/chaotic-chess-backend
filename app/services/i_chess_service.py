import abc
from typing import List

from app.dto.game_info_dto import GameInfoDTO
from app.dto.game_init_dto import GameInitDTO
from app.dto.move_dto import MoveDto
from app.dto.turn_result_dto import TurnResultDTO


class IChessService(metaclass=abc.ABCMeta):
    async def init_game(self, game_info_dto: GameInitDTO) -> GameInfoDTO:
        """
        게임을 처음 초기화 시킴

        :return:  초기화된 게임의 정보를 담은 DTO 객체
        """
        pass

    async def load_game(self, game_id: str) -> GameInfoDTO | None:
        """
        진행 중이던 게임을 불러온다

        :arg game_id: 게임의 ID 몽고DB의 ObjectId로 변환되어 사용된다.

        :return: 초기화된 게임의 정보를 담은 DTO 객체
        """
        pass

    async def take_a_turn(self, game_id: str, user_move: MoveDto) -> TurnResultDTO:
        """
        턴을 진행하는 로직이 작성된 함수

        :param game_id: 진행중인 게임의 ID
        :param user_move: 유저의 움직임의 정보를 담은 객체
        :return: GameInfoDTO ai까지 움직이고 난 후의 정보를 반환
        """
        pass

    async def get_history(self, game_id: str) -> List[str]:
        """
        현제까지의 게임에서의 이동을 받아오는 함수

        :param game_id: 게임의 ID
        :return: List[str] 대수표기법의 이동기록들이 문자열로 저장된다.
        """
        pass

    async def end_game(self, game_id: str):
        """
        게임을 끝내는 함수다.
        체크메이트나 기권뿐만이 아니라 게임을 끝내는 모든 경우를 포함한다.

        :param game_id:
        :return:
        """
        pass

    async def reset_game(self, game_id: str):
        """
        게임을 초기화한다. 처음부터 다시 시작하기 위함이다.

        :param game_id:
        :return:
        """
        pass