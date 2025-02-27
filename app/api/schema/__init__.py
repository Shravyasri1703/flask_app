from ariadne import make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
from pathlib import Path
from app.api.schema.query import query
from app.api.schema.mutation import mutation
from app.api.schema.types import types

def load_schema():
    schema_path = Path(__file__).parent / "schema.graphql"

    if schema_path.exists():
        return load_schema_from_path(str(schema_path))
    
    return """
    type User {
        id: ID!
        username: String!
        email: String!
        isActive: Boolean!
        createdAt: String!
        updatedAt: String!
    }

    type AuthPayload {
        success: Boolean!
        message: String
        user: User
        accessToken: String
        refreshToken: String
    }

    type TokenPayload {
        success: Boolean!
        message: String
        accessToken: String
    }

    type LogoutPayload {
        success: Boolean!
        message: String
    }

    type Query {
        me: User
    }

    type Mutation {
        register(username: String!, email: String!, password: String!): AuthPayload!
        login(email: String!, password: String!): AuthPayload!
        refreshToken: TokenPayload!
        logout: LogoutPayload!
    }
    """
def create_schema():
    schema = load_schema()
    return make_executable_schema(schema, query, mutation, *types)
