import unittest
import datetime

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.database import get_mongo_client
from app.schemas.chess_game_schema import ChessGameSchema


class TestMongoDB(unittest.IsolatedAsyncioTestCase):

    _mongo_client: AsyncIOMotorClient

    def setUp(self):
        self._mongo_client = get_mongo_client()

    def tearDown(self):
        self._mongo_client.close()

    async def test_ping(self):
        await self._mongo_client.admin.command('ping')
        self.assertTrue(True)

    async def test_get_date(self):
        sample_data = ChessGameSchema(
            game_status="ongoing",
            white="ai",
            moves=[
                "gen-Bb3",
                "mov-Bb3e6",
                "!mov-Bb3f1",
                "!mov-Bb3b3",
                "gen-e3",
                "mov-b3b4",
                "mov-b4c3/ep",
                "mov-Pb3b8Q",
                "mov-0-0",
                "mov-0-0-0",
                "mov-Pb3b8Q"
            ],
            current_fen = "fen",
            updated_at = datetime.datetime.now(datetime.timezone.utc)
        )

        db = self._mongo_client.get_database("chaotic_chess")
        collection = db.get_collection("chess_game")
        result_id = await collection.insert_one( sample_data.model_dump() )

        self.assertIsNotNone(result_id)

        data = await collection.find_one({
            "_id": result_id.inserted_id
        })

        self.assertIsNotNone(data)

        self.assertEqual(data['game_status'], 'ongoing')
        self.assertEqual(data['white'], 'ai')

        self.assertTrue(data is not None)

        await collection.delete_one({"_id": result_id.inserted_id})


if __name__ == '__main__':
    unittest.main()
