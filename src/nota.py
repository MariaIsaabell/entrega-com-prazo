from datetime import datetime, timedelta, timezone
from math import isfinite
from numbers import Real


def calcular_nota_final(nota, prazo, entrega, justificativa_aprovada, novo_prazo):
    """Calcula a nota final e o resultado da avaliação de uma entrega."""
    if not isinstance(nota, Real) or isinstance(nota, bool) or not isfinite(nota):
        raise ValueError("A nota deve ser um número finito entre 0 e 10.")
    if not 0 <= nota <= 10:
        raise ValueError("A nota deve estar entre 0 e 10.")
    if not isinstance(justificativa_aprovada, bool):
        raise ValueError("justificativa_aprovada deve ser um valor booleano.")
    if not isinstance(prazo, datetime) or not isinstance(entrega, datetime):
        raise ValueError("prazo e entrega devem ser datas e horas válidas.")

    if justificativa_aprovada:
        if not isinstance(novo_prazo, datetime):
            raise ValueError(
                "Uma justificativa aprovada exige um novo prazo válido."
            )
        prazo = novo_prazo

    if prazo.tzinfo != entrega.tzinfo:
        raise ValueError("prazo e entrega devem usar o mesmo fuso horário.")

    if prazo.tzinfo is not None:
        prazo_comparavel = prazo.astimezone(timezone.utc)
        entrega_comparavel = entrega.astimezone(timezone.utc)
    else:
        prazo_comparavel = prazo
        entrega_comparavel = entrega

    atraso = entrega_comparavel - prazo_comparavel
    dias_atraso = 0
    if atraso > timedelta(0):
        dias_atraso = atraso.days + int(
            atraso.seconds > 0 or atraso.microseconds > 0
        )

    desconto_percentual = min(dias_atraso * 10, 50)
    if atraso > timedelta(days=5):
        return {
            "situacao": "rejeitada",
            "nota_final": None,
            "desconto_percentual": desconto_percentual,
            "dias_atraso": dias_atraso,
        }

    nota_final = round(float(nota) * (1 - desconto_percentual / 100), 2)
    return {
        "situacao": "aceita",
        "nota_final": nota_final,
        "desconto_percentual": desconto_percentual,
        "dias_atraso": dias_atraso,
    }
