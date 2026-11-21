# Cole aqui os seus criterios de aceitacao, no formato Dado / Quando / Entao,
# um por requisito, antes de pedir qualquer teste ao Copilot.
#

# CRITÉRIOS DE ACEITAÇÃO

# RF-001
# Dado que existe um prazo e uma data e hora de entrega
# Quando a função comparar a entrega com o prazo
# Então deve identificar se a entrega foi realizada dentro do prazo ou com atraso.

# RF-002
# Dado que o aluno possui uma nota e um prazo definido
# Quando entregar o trabalho até a data e hora limite
# Então deve receber a nota integral, sem desconto.

# RF-003
# Dado que o aluno entregou o trabalho após o prazo
# Quando a função calcular a nota final
# Então deve aplicar um desconto de 10% da nota original por dia iniciado de atraso.

# RF-004
# Dado que a entrega possui mais de cinco dias de atraso
# Quando a função calcular o desconto
# Então o desconto aplicado não deve ultrapassar 50% da nota original.

# RF-005
# Dado que o aluno entregou o trabalho depois de cinco dias de atraso
# Quando a função verificar o prazo da entrega
# Então deve rejeitar a entrega.

# RF-006
# Dado que o aluno possui uma justificativa aprovada e um novo prazo definido pela coordenação
# Quando entregar o trabalho dentro do novo prazo
# Então deve receber a nota integral, sem desconto.

# RF-007
# Dado que o professor reabriu a entrega para um aluno específico e definiu um novo prazo
# Quando o sistema avaliar a entrega desse aluno
# Então deve considerar o novo prazo individual.

# RF-008
# Dado que um aluno realizou uma entrega
# Quando o sistema registrar essa entrega
# Então deve armazenar quem entregou, quando entregou e qual desconto foi aplicado.

from datetime import datetime, timedelta

import pytest

from src.nota import calcular_nota_final


def test_rf001_identifies_delivery_before_at_and_after_deadline():
    prazo = datetime(2026, 11, 20, 12, 0)

    antes = calcular_nota_final(10, prazo, prazo - timedelta(seconds=1), False, None)
    no_limite = calcular_nota_final(10, prazo, prazo, False, None)
    depois = calcular_nota_final(
        10, prazo, prazo + timedelta(seconds=1), False, None
    )

    assert antes == {
        "situacao": "aceita",
        "nota_final": 10,
        "desconto_percentual": 0,
        "dias_atraso": 0,
    }
    assert no_limite == {
        "situacao": "aceita",
        "nota_final": 10,
        "desconto_percentual": 0,
        "dias_atraso": 0,
    }
    assert depois == {
        "situacao": "aceita",
        "nota_final": 9,
        "desconto_percentual": 10,
        "dias_atraso": 1,
    }


@pytest.mark.parametrize("antecedencia", [timedelta(seconds=1), timedelta(0)])
def test_rf002_delivery_before_or_at_deadline_receives_full_grade(antecedencia):
    prazo = datetime(2026, 11, 20, 12, 0)

    resultado = calcular_nota_final(
        10, prazo, prazo - antecedencia, False, None
    )

    assert resultado == {
        "situacao": "aceita",
        "nota_final": 10,
        "desconto_percentual": 0,
        "dias_atraso": 0,
    }


@pytest.mark.parametrize(
    ("atraso", "nota_esperada", "dias_atraso"),
    [
        (timedelta(seconds=1), 9, 1),
        (timedelta(days=1, seconds=1), 8, 2),
    ],
)
def test_rf003_deducts_ten_percent_per_started_day(
    atraso, nota_esperada, dias_atraso
):
    prazo = datetime(2026, 11, 20, 12, 0)

    resultado = calcular_nota_final(10, prazo, prazo + atraso, False, None)

    assert resultado == {
        "situacao": "aceita",
        "nota_final": nota_esperada,
        "desconto_percentual": dias_atraso * 10,
        "dias_atraso": dias_atraso,
    }


def test_rf004_discount_is_capped_at_fifty_percent_at_five_day_boundary():
    prazo = datetime(2026, 11, 20, 12, 0)

    resultado = calcular_nota_final(
        10, prazo, prazo + timedelta(days=5), False, None
    )

    assert resultado == {
        "situacao": "aceita",
        "nota_final": 5,
        "desconto_percentual": 50,
        "dias_atraso": 5,
    }


def test_rf005_rejects_delivery_more_than_five_days_late():
    prazo = datetime(2026, 11, 20, 12, 0)

    resultado = calcular_nota_final(
        10, prazo, prazo + timedelta(days=5, seconds=1), False, None
    )

    assert set(resultado) == {
        "situacao",
        "nota_final",
        "desconto_percentual",
        "dias_atraso",
    }
    assert resultado["situacao"] == "rejeitada"
    assert resultado["nota_final"] is None
    assert resultado["dias_atraso"] == 6


def test_rf006_approved_justification_uses_new_deadline():
    prazo = datetime(2026, 11, 20, 12, 0)
    novo_prazo = prazo + timedelta(days=3)
    entrega = novo_prazo

    resultado = calcular_nota_final(10, prazo, entrega, True, novo_prazo)

    assert resultado == {
        "situacao": "aceita",
        "nota_final": 10,
        "desconto_percentual": 0,
        "dias_atraso": 0,
    }


def test_rf007_reopened_deadline_is_individual_to_student():
    pytest.skip(
        "A função não recebe a identificação do aluno nem dados de reabertura; "
        "não pode verificar se o novo prazo se aplica somente a esse aluno."
    )


def test_rf008_records_delivery_and_applied_discount():
    pytest.skip(
        "A função calcula a nota e não possui interface de armazenamento ou "
        "registro da entrega."
    )
