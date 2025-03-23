from dependency_injector import containers, providers

from app.core.database import get_mongo_client
from app.repositories.chess_repository import ChessRepository


class Container(containers.DeclarativeContainer):
    mongo_client = providers.Singleton(get_mongo_client)
    chess_repository = providers.Singleton(ChessRepository, mongo_client)