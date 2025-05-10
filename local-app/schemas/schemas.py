from marshmallow import Schema, fields


class ModelSchema(Schema):
    model = fields.String(
        required=True, description="Nome do modelo a ser criado", example="llama3.1:8b"
    )


class MessageSchema(Schema):
    role = fields.String(
        required=True,
        description="O papel da mensagem (ex: user, system)",
        example="user",
    )
    content = fields.String(
        required=True,
        description="Conteúdo da mensagem",
        example="Qual é a capital do Brasil?",
    )


class ChatRequestSchema(Schema):
    model = fields.String(
        required=True, description="Nome do modelo", example="llama3.1:8b"
    )
    messages = fields.List(
        fields.Nested(MessageSchema),
        required=True,
        description="Mensagens para o modelo",
        example=[{"role": "user", "content": "Qual a capital do Brasil?"}],
    )
    options = fields.Dict(
        keys=fields.String(),
        values=fields.Raw(),
        description="Parâmetros opcionais do modelo",
        example={"temperature": 0.8, "top_k": 30},
    )
