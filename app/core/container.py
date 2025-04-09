from dependency_injector import containers, providers

from app.core.database import get_mongo_client
from app.repositories.chess_repository import ChessRepository
from app.repositories.i_chess_repository import IChessRepository
from app.services.ai_service import AIService
from app.services.chess_service import ChessService


class Container(containers.DeclarativeContainer):
    mongo_client = providers.Singleton(get_mongo_client)
    chess_repository: IChessRepository = providers.Singleton(ChessRepository, mongo_client)
    ai_service: AIService = providers.Singleton(AIService, mongo_client)
    chess_service: ChessService = providers.Singleton(ChessService, chess_repository, mongo_client)