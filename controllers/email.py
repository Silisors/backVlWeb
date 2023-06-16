from fastapi import APIRouter
from type.email import Mutation, Query
from strawberry.asgi import GraphQL
import strawberry

email = APIRouter()

schema = strawberry.Schema(Query, Mutation)
graphql_app = GraphQL(schema)

email.add_route("/graphql", graphql_app)