from typing import List

from pydantic import BaseModel, Field

from app.domain.game import Game


class DBUpdateWithMovingDto(BaseModel):
    moves: List[str]
    new_fen: str


# Game으로 부터최근 N턴간의 기록을 얻어 옴
# move_cnt의 기본값은 2인데 이는 최근 한턴(백과 흑 한번씩 움진인)움직임을 가져오라는 것임
# 이 함수는 몽고DB에 저장할 때 사용하기 위해 만들어진 것으로 (한턴에 한번씩 저장한다는 전제하에) 기본값 2를 사용하는 일이 많을 것으로 생각됨
def to_db_update_with_moving_dto(game: Game, move_cnt: int = 2):
    return DBUpdateWithMovingDto(
        moves=game.moves[-move_cnt:],
        new_fen=game.board.fen()
    )
