import unittest
from typing import List

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.database import get_mongo_client
from app.domain.chess_game import ChessGame
from app.domain.turn import MoveResult
from app.dto.game_info_dto import from_chess_game_schema
from app.dto.game_init_dto import GameInitDTO
from app.dto.move_dto import MoveDto
from app.repositories.chess_repository import ChessRepository
from app.schemas.chess_game_schema import ChessGameSchema
from app.services.ai_service import AIService
from app.services.chess_service import ChessService


class ChessServiceTest(unittest.IsolatedAsyncioTestCase):
    _mongo_client: AsyncIOMotorClient
    _chess_repository: ChessRepository
    _chess_service: ChessService

    def setUp(self):
        self._mongo_client = get_mongo_client()
        self._chess_repository = ChessRepository(self._mongo_client)
        self._chess_service = ChessService(self._chess_repository, AIService())

    def tearDown(self):
        self._mongo_client.close()

    async def test_game_init(self):
        result = await self._chess_service.init_game(GameInitDTO(
            first="ai"
        ))
        game_data_from_repository = await self._chess_repository.get_by_id(result.game_id)
        await self._chess_repository.delete_data(result.game_id)
        self.assertEqual(result.white, "ai")
        self.assertEqual(result.moves, [])
        self.assertTrue(result.fen.startswith("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"))
        self.assertIsNotNone(result.game_id)
        self.assertEqual(await from_chess_game_schema(game_data_from_repository), result)

    async def test_load_game(self):
        result = await self._chess_service.init_game(GameInitDTO(first="user"))
        loaded_game_data = await self._chess_service.load_game(result.game_id)
        await self._chess_repository.delete_data(result.game_id)
        self.assertEqual(result, loaded_game_data)

    async def test_try_load_game_with_wrong_id(self):
        loaded_game = await self._chess_service.load_game("123456789012345678901234")
        self.assertIsNone(loaded_game)

    async def test_take_a_turn(self):
        game_info = await self._chess_service.init_game(GameInitDTO(first="user"))
        result = await self._chess_service.take_a_turn(game_info.game_id, MoveDto(moving="Pb2b4"))
        self.assertEqual(len(result.game_info.moves), len(game_info.moves) + 2)
        game_info_from_db = await from_chess_game_schema(await self._chess_repository.get_by_id(game_info.game_id))
        await self._chess_repository.delete_data(game_info.game_id)
        self.assertEqual(game_info_from_db, result.game_info)

    async def test_get_history(self):
        test_id = await self._chess_repository.save(ChessGameSchema(
            white="ai",
            moves=["1", "2", "3", "4", "5"],
            current_fen="no",
            game_status="ongoing"
        ))
        result = await self._chess_service.get_history(test_id)
        await self._chess_repository.delete_data(test_id)

        self.assertIsInstance(result, List)
        self.assertIsInstance(result[0], str)
        self.assertEqual(result, ["1", "2", "3", "4", "5"])

    async def test_end_game(self):
        test_id = (await self._chess_service.init_game(GameInitDTO(first="user"))).game_id
        await self._chess_repository.end_game(test_id)
        game = await self._chess_repository.get_by_id(test_id)
        await self._chess_repository.delete_data(test_id)
        self.assertEqual(game.game_status, "finished")

    async def test_game_reset(self):
        test_id = await self._chess_repository.save(ChessGameSchema(
            white="ai",
            moves=["1", "2", "3", "4", "5"],
            current_fen="no",
            game_status="ongoing"
        ))
        await self._chess_service.reset_game(test_id)
        game = await self._chess_repository.get_by_id(test_id)
        await self._chess_repository.delete_data(test_id)
        self.assertEqual(len(game.moves), 0)

    async def test_user_kill_king(self):
        chess_game = ChessGame(ChessGameSchema(
            game_status="ongoing",
            white="user",
            moves=[],
            current_fen="rnbqkbnr/pppppPpp/8/8/8/8/PPPPP1PP/RNBQKBNR w"
        ))
        result = await self._chess_service._take_a_move(chess_game, MoveDto(moving="f7e8"))
        self.assertEqual(len(result.moves), 1)
        self.assertEqual(result.move_result, MoveResult.USER_LOSE_CUZ_KILL_KING)
        self.assertIsNone(result.ai_message)

    async def test_user_checkmated(self):
        chess_game = ChessGame(ChessGameSchema(
            game_status="ongoing",
            white="user",
            moves=[],
            current_fen="k7/7R/8/8/8/8/8/6R1 w"
        ))
        result = await self._chess_service._take_a_move(chess_game, MoveDto(moving="Rg1g8"))
        self.assertEqual(len(result.moves), 1)
        self.assertEqual(result.move_result, MoveResult.CHECKMATE_USER_WIN)
        self.assertIsNone(result.ai_message)

if __name__ == '__main__':
    unittest.main()
