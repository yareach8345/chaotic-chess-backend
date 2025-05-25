import datetime

from bson import ObjectId
from chess import Board
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from app.dto.db_update_dto import DBUpdateWithMovingDto
from app.repositories.i_chess_repository import IChessRepository
from app.schemas.chess_game_schema import ChessGameSchema

class ChessRepository(IChessRepository):
    _chess_collection: AsyncIOMotorCollection

    def __init__(self, mongo_client: AsyncIOMotorClient):
        self._chess_collection = mongo_client.get_database("chaotic_chess").get_collection("chess_game")

    async def set_updated_time_now(self, chess_game_id: str):
        await self._chess_collection.update_one(
            {"_id": chess_game_id},
            {"$set": {"updated_time": datetime.datetime.now(datetime.UTC)}},
        )

    # 데이터를 저장하는데 쓰임
    # 데이터를 처음 생성하는 경우에는 chess_game_schema의 id를 None으로 해둘 것
    # 데이터를 갱신하는 경우에는 chess_game_schema를 기존의 document의 _id로 해둘 것
    async def save(self, chess_game_schema: ChessGameSchema) -> str:
        insert_result = await self._chess_collection.insert_one( chess_game_schema.model_dump() )
        return str(insert_result.inserted_id)

    # 데이터를 불러오는데 쓰임
    # 매개변수로 불러올 id값을 str으로 전달한다.
    # id에 해당하는 값이 없을 시에는 None이 반환된다.
    async def get_by_id(self, chess_game_id: str) -> ChessGameSchema | None:
        await self.set_updated_time_now(chess_game_id)
        result = await self._chess_collection.find_one( {"_id": ObjectId(chess_game_id)} )
        if result is None:
            return None
        result["_id"] = str(result["_id"])
        return ChessGameSchema(**result)

    # 기물의 움직임에 의한 갱신
    # moves에는 기물이 이동한 기록이
    # new_fen에는 현제 채스판의 모습이 fen 표기법으로 기록되어 있어야 한다.
    async def update_by_moving(self, chess_game_id: str, chess_move_dto: DBUpdateWithMovingDto):
        result = await self._chess_collection.update_one(
            { "_id": ObjectId(chess_game_id), },
            {
                "$set": { "current_fen": chess_move_dto.new_fen, "updated_at": datetime.datetime.now(datetime.UTC) },
                "$push": { "moves": { "$each": chess_move_dto.moves } }
            }
        )
        return str(result.upserted_id)

    # 데이터를 삭제한다.
    # 주의: 이 작업이 이루어지고 난 후에는 클라이언트에서 데이터를 불러올 수 없다.
    # 게임이 종료되거나 하여 클라이언트 측에서 다시 불러올 일이 없을 때만 사용할 것
    async def delete_data(self, chess_game_id: str):
        result = await self._chess_collection.delete_one({ "_id": ObjectId(chess_game_id) })
        return result.deleted_count != 0

    async def end_game(self, chess_game_id: str, result: str = "finished"):
        await self._chess_collection.update_one( { "_id": ObjectId(chess_game_id) }, { "$set" : {"game_status": result, "updated_at": datetime.datetime.now(datetime.UTC) }} )

    async def reset_game(self, chess_game_id: str):
        await self._chess_collection.update_one(
            {"_id": ObjectId(chess_game_id)},
            {
                "$set": {
                    "game_status": "ongoing",
                    "moves": [],
                    "current_fen": Board().fen(),
                    "updated_at": datetime.datetime.now(datetime.UTC)
                },
            }
        )
