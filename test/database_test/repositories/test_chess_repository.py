import unittest
from datetime import datetime, UTC

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.database import get_mongo_client
from app.dto.db_update_dto import DBUpdateWithMovingDto
from app.repositories.chess_repository import ChessRepository
from app.schemas.chess_game_schema import ChessGameSchema


class TestChessRepository(unittest.IsolatedAsyncioTestCase):

    _database: AsyncIOMotorClient
    _repository: ChessRepository
    _id: str | None

    sample_data = ChessGameSchema(
        game_status="ongoing",
        white="ai",
        moves=[],
        updated_at=datetime.now(UTC),
        current_fen="k7/8/8/8/8/8/8/6RK b - - 99 100"
    )

    async def asyncSetUp(self):
        self._database = get_mongo_client()
        self._repository = ChessRepository(self._database)
        self._id = await self._repository.save(self.sample_data)

    async def asyncTearDown(self):
        if self._id is not None:
            await self._repository._chess_collection.delete_one({"_id": self._id})
        self._database.close()

    async def test_save(self):
        self.assertTrue(type(self._id) is str)

    async def test_get_by_id(self):
        data = await self._repository.get_by_id(self._id)
        self.assertIsNotNone(data)
        self.assertEqual(data.id, self._id)
        self.assertEqual(data.game_status, "ongoing")
        self.assertEqual(len(data.moves), 0)

    async def test_get_by_id_with_not_exists_id(self):
        data = await self._repository.get_by_id(str(ObjectId()))
        self.assertIsNone(data)

    async def test_update(self):
        await self._repository.update_by_moving(
            self._id,
            DBUpdateWithMovingDto(
                moves=["mov-Rg1g8"],
                new_fen="k5R1/8/8/8/8/8/8/7K b - - 101 100"
            )
        )
        data = await self._repository.get_by_id(self._id)
        self.assertIsNotNone(data)
        self.assertEqual(data.id, self._id)
        self.assertEqual(data.game_status, "ongoing")
        self.assertEqual(len(data.moves), 1)

    async def test_delete(self):
        delete_result = await self._repository.delete_data(self._id)
        self.assertTrue(delete_result, 1)
        get_result = await self._repository.get_by_id(self._id)
        self.assertIsNone(get_result)
        self._id = None

    async def test_check_game_is_exist(self):
        result = await self._repository.check_game_is_exist(self._id)
        self.assertTrue(result)

    async def test_check_game_is_not_exist(self):
        result = await self._repository.check_game_is_exist(str(ObjectId()))
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()