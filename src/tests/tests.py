"""
tests.py — Suite de testes para parser e roller de dados.

Estrutura:
  PARTE 1 — Parser
    1a. Strings que devem ser aceitas (parse + validação OK)
    1b. Strings que devem ser rejeitadas (erro de sintaxe)
  PARTE 2 — Resolução
    Usa as mesmas strings da parte 1a com seed fixo e verifica
    tipo de resultado, shape e propriedades do log.

Os testes chamam execute_command diretamente, que retorna:
  [True,  result, log_str]  → sucesso
  [False, None,  msg]       → erro de sintaxe / validação
"""

import random
import unittest

# Ajuste o import conforme a estrutura do seu projeto
from ..roller import execute_command


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def run(cmd: str):
    """Executa um comando e retorna (ok, result, log)."""
    return execute_command(cmd)


def assertPasses(tc: unittest.TestCase, cmd: str):
    ok, result, log = run(cmd)
    tc.assertTrue(ok, msg=f"{cmd!r} deveria passar, mas falhou com: {log}")
    return result, log


def assertFails(tc: unittest.TestCase, cmd: str):
    ok, result, log = run(cmd)
    tc.assertFalse(ok, msg=f"{cmd!r} deveria falhar, mas passou com result={result}")
    return log


# ─────────────────────────────────────────────────────────────────────────────
# PARTE 1a — Parser: strings que devem ser aceitas
# ─────────────────────────────────────────────────────────────────────────────

class TestParserValid(unittest.TestCase):

    # ── Dados básicos ─────────────────────────────────────────────────────────

    def test_dado_simples_d6(self):
        assertPasses(self, "d6")

    def test_dado_simples_d20(self):
        assertPasses(self, "d20")

    def test_dado_fudge(self):
        assertPasses(self, "3df")

    def test_dado_multiplo(self):
        assertPasses(self, "4d8")

    def test_dois_dados_diferentes(self):
        assertPasses(self, "2d20")

    # ── Aritmética ────────────────────────────────────────────────────────────

    def test_dado_mais_inteiro(self):
        assertPasses(self, "4d8 + 1")

    def test_inteiro_menos_dado(self):
        assertPasses(self, "2 - 3d10")

    def test_dado_mais_constante(self):
        assertPasses(self, "2d6 + 3")

    def test_dado_menos_constante(self):
        assertPasses(self, "3d4 - 1")

    def test_soma_dois_dados(self):
        assertPasses(self, "2d20 + 3d4")

    # ── kh: variações de keep count ───────────────────────────────────────────

    def test_kh_keep_1(self):
        assertPasses(self, "4d6 | kh:1")

    def test_kh_keep_2(self):
        assertPasses(self, "4d6 | kh:2")

    def test_kh_keep_3(self):
        assertPasses(self, "4d6 | kh:3")

    # ── kl: variações de keep count ───────────────────────────────────────────

    def test_kl_keep_1(self):
        assertPasses(self, "4d6 | kl:1")

    def test_kl_keep_2(self):
        assertPasses(self, "4d6 | kl:2")

    def test_kl_keep_3(self):
        assertPasses(self, "4d6 | kl:3")

    # ── kh/kl + aritmética ───────────────────────────────────────────────────

    def test_kh_mais_inteiro(self):
        assertPasses(self, "4d6 | kh:2 + 4")

    def test_kl_menos_inteiro(self):
        assertPasses(self, "4d6 | kl:2 - 1")

    def test_dado_mais_dado_kh(self):
        assertPasses(self, "5d6 + 1d4 | kh:3")

    def test_dado_mais_dado_kl(self):
        assertPasses(self, "5d6 + 1d4 | kl:2")

    # ── ex: todas as condições ────────────────────────────────────────────────

    def test_ex_igual_implicito(self):
        assertPasses(self, "3d12 | ex:12")

    def test_ex_igual_explicito(self):
        assertPasses(self, "3d12 | ex:=12")

    def test_ex_diferente(self):
        assertPasses(self, "3d12 | ex:!=1")

    def test_ex_maior(self):
        assertPasses(self, "3d6 | ex:>5")

    def test_ex_maior_igual(self):
        assertPasses(self, "3d6 | ex:>=6")

    def test_ex_menor(self):
        assertPasses(self, "3d6 | ex:<2")

    def test_ex_menor_igual(self):
        assertPasses(self, "3d6 | ex:<=1")

    def test_ex_range(self):
        assertPasses(self, "3d10 | ex:8..10")

    def test_ex_lista(self):
        assertPasses(self, "3d6 | ex:5,6")

    # ── rr: todas as condições ────────────────────────────────────────────────

    def test_rr_igual_implicito(self):
        assertPasses(self, "3d12 | rr:1")

    def test_rr_igual_explicito(self):
        assertPasses(self, "3d12 | rr:=1")

    def test_rr_diferente(self):
        assertPasses(self, "3d12 | rr:!=12")

    def test_rr_maior(self):
        assertPasses(self, "3d6 | rr:>5")

    def test_rr_maior_igual(self):
        assertPasses(self, "3d6 | rr:>=6")

    def test_rr_menor(self):
        assertPasses(self, "3d6 | rr:<2")

    def test_rr_menor_igual(self):
        assertPasses(self, "3d6 | rr:<=1")

    def test_rr_range(self):
        assertPasses(self, "3d10 | rr:1..3")

    def test_rr_lista(self):
        assertPasses(self, "3d6 | rr:1,2")

    # ── cn: todas as condições ────────────────────────────────────────────────

    def test_cn_igual_implicito(self):
        assertPasses(self, "3d12 | cn:6")

    def test_cn_igual_explicito(self):
        assertPasses(self, "3d12 | cn:=6")

    def test_cn_diferente(self):
        assertPasses(self, "3d12 | cn:!=6")

    def test_cn_maior(self):
        assertPasses(self, "3d12 | cn:>6")

    def test_cn_maior_igual(self):
        assertPasses(self, "3d12 | cn:>=6")

    def test_cn_menor(self):
        assertPasses(self, "3d12 | cn:<6")

    def test_cn_menor_igual(self):
        assertPasses(self, "3d12 | cn:<=6")

    def test_cn_range(self):
        assertPasses(self, "3d10 | cn:5..8")

    def test_cn_lista(self):
        assertPasses(self, "3d6 | cn:5,6")

    # ── cn + aritmética ───────────────────────────────────────────────────────

    def test_cn_mais_inteiro(self):
        assertPasses(self, "3d12 | cn:>6 + 1")

    def test_cn_menos_inteiro(self):
        assertPasses(self, "2d10 | cn:8..10 - 5")

    # ── ex/rr + aritmética ────────────────────────────────────────────────────

    def test_ex_mais_inteiro(self):
        assertPasses(self, "3d6 | ex:6 + 2")

    def test_rr_menos_inteiro(self):
        assertPasses(self, "3d6 | rr:1 - 1")

    # ── Encadeamentos duplos ──────────────────────────────────────────────────

    def test_kh_cn(self):
        assertPasses(self, "4d6 | kh:2 | cn:6")

    def test_kh_ex(self):
        assertPasses(self, "4d6 | kh:2 | ex:>5")

    def test_kh_rr(self):
        assertPasses(self, "4d6 | kh:2 | rr:1")

    def test_kl_cn(self):
        assertPasses(self, "4d6 | kl:2 | cn:1")

    def test_kl_ex(self):
        assertPasses(self, "4d6 | kl:2 | ex:<2")

    def test_kl_rr(self):
        assertPasses(self, "4d6 | kl:2 | rr:1")

    def test_ex_cn(self):
        assertPasses(self, "3d6 | ex:6 | cn:6")

    def test_ex_kh(self):
        assertPasses(self, "3d6 | ex:6 | kh:2")

    def test_ex_kl(self):
        assertPasses(self, "3d6 | ex:6 | kl:1")

    def test_ex_rr(self):
        assertPasses(self, "3d6 | ex:6 | rr:1")

    def test_rr_cn(self):
        assertPasses(self, "3d6 | rr:1 | cn:>3")

    def test_rr_kh(self):
        assertPasses(self, "3d6 | rr:1 | kh:2")

    def test_rr_kl(self):
        assertPasses(self, "3d6 | rr:1 | kl:1")

    def test_rr_ex(self):
        assertPasses(self, "3d6 | rr:1 | ex:6")

    # ── Encadeamentos triplos ─────────────────────────────────────────────────

    def test_kh_ex_cn(self):
        assertPasses(self, "4d6 | kh:3 | ex:6 | cn:6")

    def test_kh_rr_cn(self):
        assertPasses(self, "4d6 | kh:3 | rr:1 | cn:>4")

    def test_ex_kh_cn(self):
        assertPasses(self, "4d6 | ex:6 | kh:3 | cn:6")

    def test_rr_kh_cn(self):
        assertPasses(self, "4d6 | rr:1 | kh:3 | cn:>4")

    # ── Operadores com múltiplos dados e funções ──────────────────────────────

    def test_kl_mais_kh(self):
        assertPasses(self, "4d6 | kl:2 + 5d10 | kh:4")

    def test_rr_mais_ex(self):
        assertPasses(self, "3d6 | rr:1 + 1d10 | ex:10")

    # ── mr simples ────────────────────────────────────────────────────────────

    def test_mr_dado_simples(self):
        assertPasses(self, "2d6 | mr:3")

    def test_mr_d20(self):
        assertPasses(self, "d20 | mr:4")

    # ── mr com função ─────────────────────────────────────────────────────────

    def test_mr_com_kh(self):
        assertPasses(self, "4d6 | kh:3 | mr:6")

    def test_mr_com_rr(self):
        assertPasses(self, "3d6 | rr:1 | mr:3")

    def test_mr_com_ex(self):
        assertPasses(self, "2d8 | ex:>7 | mr:4")

    def test_mr_com_cn(self):
        assertPasses(self, "3d6 | cn:>4 | mr:3")

    # ── mr com aritmética ─────────────────────────────────────────────────────

    def test_mr_soma_inteiro(self):
        assertPasses(self, "5d6 + 1 | mr:2")

    def test_mr_kh_soma_inteiro(self):
        assertPasses(self, "4d6 | kh:3 + 2 | mr:3")

    def test_mr_menos_inteiro(self):
        assertPasses(self, "3d6 - 1 | mr:4")


# ─────────────────────────────────────────────────────────────────────────────
# PARTE 1b — Parser: strings que devem ser rejeitadas
# ─────────────────────────────────────────────────────────────────────────────

class TestParserInvalid(unittest.TestCase):

    # ── Dados inválidos ───────────────────────────────────────────────────────

    def test_dado_zero_faces(self):
        """d0 não é um dado válido."""
        assertFails(self, "1d0")

    def test_dado_zero_quantidade(self):
        """0d6 não é válido — quantidade mínima é 1."""
        assertFails(self, "0d6")

    # ── kh: omitir elementos obrigatórios ────────────────────────────────────

    def test_kh_sem_valor(self):
        """kh sem valor após ':' deve falhar."""
        assertFails(self, "4d6 | kh:")

    def test_kh_valor_zero(self):
        """kh:0 — manter 0 dados não faz sentido."""
        assertFails(self, "4d6 | kh:0")

    def test_kh_valor_nao_inteiro(self):
        """kh:1.5 — valor deve ser inteiro."""
        assertFails(self, "4d6 | kh:1.5")

    def test_kh_sobre_inteiro_literal(self):
        """kh não pode operar sobre inteiro literal após operador."""
        assertFails(self, "5d6 + 1 | kh:3")

    # ── kl: omitir elementos obrigatórios ────────────────────────────────────

    def test_kl_sem_valor(self):
        """kl sem valor após ':' deve falhar."""
        assertFails(self, "4d6 | kl:")

    def test_kl_valor_zero(self):
        """kl:0 — manter 0 dados não faz sentido."""
        assertFails(self, "4d6 | kl:0")

    def test_kl_valor_nao_inteiro(self):
        """kl:1.5 — valor deve ser inteiro."""
        assertFails(self, "4d6 | kl:1.5")

    def test_kl_sobre_inteiro_literal(self):
        """kl não pode operar sobre inteiro literal após operador."""
        assertFails(self, "5d6 + 1 | kl:3")

    # ── ex: omitir elementos obrigatórios ────────────────────────────────────

    def test_ex_sem_valor(self):
        """ex sem valor após ':' deve falhar."""
        assertFails(self, "3d6 | ex:")

    def test_ex_sobre_inteiro_literal(self):
        """ex não pode operar sobre inteiro literal após operador."""
        assertFails(self, "5d6 + 1 | ex:3")

    # ── rr: omitir elementos obrigatórios ────────────────────────────────────

    def test_rr_sem_valor(self):
        """rr sem valor após ':' deve falhar."""
        assertFails(self, "3d6 | rr:")

    def test_rr_sobre_inteiro_literal(self):
        """rr não pode operar sobre inteiro literal após operador."""
        assertFails(self, "5d6 + 1 | rr:3")

    # ── cn: omitir elementos obrigatórios ────────────────────────────────────

    def test_cn_sem_valor(self):
        """cn sem valor após ':' deve falhar."""
        assertFails(self, "3d6 | cn:")

    def test_cn_sobre_inteiro_literal(self):
        """cn não pode operar sobre inteiro literal após operador."""
        assertFails(self, "5d6 + 1 | cn:3")

    def test_cn_sobre_inteiro_direto(self):
        """cn não pode receber inteiro literal como argumento direto."""
        assertFails(self, "1 | cn:>3")

    # ── mr: omitir elementos obrigatórios ────────────────────────────────────

    def test_mr_sem_valor(self):
        """mr sem valor após ':' deve falhar."""
        assertFails(self, "3d6 | mr:")

    def test_mr_sobre_inteiro_literal(self):
        """mr não pode operar sobre inteiro literal."""
        assertFails(self, "2 | mr:4")

    def test_mr_nao_terminal(self):
        """mr deve ser sempre o último elemento — função após mr é inválida."""
        assertFails(self, "4d6 | mr:3 | kh:2")

    # ── função desconhecida ───────────────────────────────────────────────────

    def test_funcao_desconhecida(self):
        """Função inexistente deve ser rejeitada."""
        assertFails(self, "3d6 | xyz:5")


# ─────────────────────────────────────────────────────────────────────────────
# PARTE 2 — Resolução
# Usa seed fixo para resultados reproduzíveis.
# Não verifica valores exatos (rolagem é aleatória); verifica:
#   - execute_command retorna True
#   - result é do tipo correto (int para comandos normais, list para mr)
#   - result está dentro do intervalo possível dos dados
#   - log é uma string não vazia
# Para mr: verifica shape (tamanho da lista) e que cada elemento é int.
# ─────────────────────────────────────────────────────────────────────────────

SEED = 42


class TestResolution(unittest.TestCase):

    def setUp(self):
        random.seed(SEED)

    # ── Helper de verificação ─────────────────────────────────────────────────

    def _check(self, cmd, *, min_result=None, max_result=None, is_list=False,
               list_len=None, log_contains=None):
        ok, result, log = run(cmd)
        self.assertTrue(ok, msg=f"{cmd!r} falhou: {log}")
        self.assertIsInstance(log, str)
        self.assertGreater(len(log), 0)

        if is_list:
            self.assertIsInstance(result, list, msg=f"{cmd!r}: result deveria ser list")
            if list_len is not None:
                self.assertEqual(len(result), list_len,
                                 msg=f"{cmd!r}: esperava lista de tamanho {list_len}")
            for i, v in enumerate(result):
                self.assertIsInstance(v, int,
                                      msg=f"{cmd!r}: item {i} deveria ser int, é {type(v)}")
        else:
            self.assertIsInstance(result, int,
                                  msg=f"{cmd!r}: result deveria ser int, é {type(result)}")
            if min_result is not None:
                self.assertGreaterEqual(result, min_result,
                                        msg=f"{cmd!r}: result={result} < min={min_result}")
            if max_result is not None:
                self.assertLessEqual(result, max_result,
                                     msg=f"{cmd!r}: result={result} > max={max_result}")

        if log_contains is not None:
            for fragment in log_contains:
                self.assertIn(fragment, log,
                              msg=f"{cmd!r}: log não contém {fragment!r}")

    # ── Dados básicos ─────────────────────────────────────────────────────────

    def test_res_d6(self):
        self._check("d6", min_result=1, max_result=6)

    def test_res_d20(self):
        self._check("d20", min_result=1, max_result=20)

    def test_res_fudge(self):
        # df resulta em -1, 0, ou 1; 3df → -3..3
        self._check("3df", min_result=-3, max_result=3)

    def test_res_4d8(self):
        self._check("4d8", min_result=4, max_result=32)

    def test_res_2d20(self):
        self._check("2d20", min_result=2, max_result=40)

    # ── Aritmética ────────────────────────────────────────────────────────────

    def test_res_dado_mais_inteiro(self):
        # 4d8 + 1 → 5..33
        self._check("4d8 + 1", min_result=5, max_result=33)

    def test_res_inteiro_menos_dado(self):
        # 2 - 3d10 → 2-30..-28
        self._check("2 - 3d10", min_result=2 - 30, max_result=2 - 3)

    def test_res_soma_dois_dados(self):
        # 2d20 + 3d4 → 5..52
        self._check("2d20 + 3d4", min_result=5, max_result=52)

    def test_res_log_operador_contem_sinal(self):
        self._check("2d6 + 3", log_contains=["+"])

    # ── kh ───────────────────────────────────────────────────────────────────

    def test_res_kh1(self):
        # kh:1 de 4d6 → 1..6
        self._check("4d6 | kh:1", min_result=1, max_result=6)

    def test_res_kh2(self):
        # kh:2 de 4d6 → 2..12
        self._check("4d6 | kh:2", min_result=2, max_result=12)

    def test_res_kh3(self):
        # kh:3 de 4d6 → 3..18
        self._check("4d6 | kh:3", min_result=3, max_result=18)

    def test_res_kh_log(self):
        self._check("4d6 | kh:2", log_contains=["Keep", "highest"])

    def test_res_kh_mais_inteiro(self):
        # kh:2 de 4d6 → 2..12, +4 → 6..16
        self._check("4d6 | kh:2 + 4", min_result=6, max_result=16)

    # ── kl ───────────────────────────────────────────────────────────────────

    def test_res_kl1(self):
        # kl:1 de 4d6 → 1..6
        self._check("4d6 | kl:1", min_result=1, max_result=6)

    def test_res_kl2(self):
        # kl:2 de 4d6 → 2..12
        self._check("4d6 | kl:2", min_result=2, max_result=12)

    def test_res_kl_log(self):
        self._check("4d6 | kl:2", log_contains=["Keep", "lowest"])

    def test_res_kl_menos_inteiro(self):
        # kl:2 de 4d6 → 2..12, -1 → 1..11
        self._check("4d6 | kl:2 - 1", min_result=1, max_result=11)

    # ── ex ───────────────────────────────────────────────────────────────────

    def test_res_ex_resultado_nao_negativo(self):
        # ex nunca reduz o pool, então soma ≥ soma mínima original
        self._check("3d6 | ex:6", min_result=3)

    def test_res_ex_log(self):
        self._check("3d6 | ex:6", log_contains=["Explode"])

    def test_res_ex_todas_condicoes(self):
        for cmd, lo, hi in [
            ("3d12 | ex:12",    3,  None),
            ("3d12 | ex:=12",   3,  None),
            ("3d12 | ex:!=1",   3,  None),
            ("3d6  | ex:>5",    3,  None),
            ("3d6  | ex:>=6",   3,  None),
            ("3d6  | ex:<2",    3,  None),
            ("3d6  | ex:<=1",   3,  None),
            ("3d10 | ex:8..10", 3,  None),
            ("3d6  | ex:5,6",   3,  None),
        ]:
            with self.subTest(cmd=cmd):
                self._check(cmd, min_result=lo, max_result=hi)

    # ── rr ───────────────────────────────────────────────────────────────────

    def test_res_rr_resultado_positivo(self):
        self._check("3d6 | rr:1", min_result=3, max_result=18)

    def test_res_rr_log(self):
        self._check("3d6 | rr:1", log_contains=["Reroll"])

    def test_res_rr_todas_condicoes(self):
        for cmd, lo, hi in [
            ("3d12 | rr:1",      3, 36),
            ("3d12 | rr:=1",     3, 36),
            ("3d12 | rr:!=12",   3, 36),
            ("3d6  | rr:>5",     3, 18),
            ("3d6  | rr:>=6",    3, 18),
            ("3d6  | rr:<2",     3, 18),
            ("3d6  | rr:<=1",    3, 18),
            ("3d10 | rr:1..3",   3, 30),
            ("3d6  | rr:1,2",    3, 18),
        ]:
            with self.subTest(cmd=cmd):
                self._check(cmd, min_result=lo, max_result=hi)

    # ── cn ───────────────────────────────────────────────────────────────────

    def test_res_cn_resultado_e_contagem(self):
        # cn retorna contagem (0..N)
        self._check("3d12 | cn:6", min_result=0, max_result=3)

    def test_res_cn_log(self):
        self._check("3d12 | cn:6", log_contains=["Count"])

    def test_res_cn_todas_condicoes(self):
        for cmd, lo, hi in [
            ("3d12 | cn:6",    0, 3),
            ("3d12 | cn:=6",   0, 3),
            ("3d12 | cn:!=6",  0, 3),
            ("3d12 | cn:>6",   0, 3),
            ("3d12 | cn:>=6",  0, 3),
            ("3d12 | cn:<6",   0, 3),
            ("3d12 | cn:<=6",  0, 3),
            ("3d10 | cn:5..8", 0, 3),
            ("3d6  | cn:5,6",  0, 3),
        ]:
            with self.subTest(cmd=cmd):
                self._check(cmd, min_result=lo, max_result=hi)

    def test_res_cn_mais_inteiro(self):
        # cn:>6 em 3d12 → 0..3, +1 → 1..4
        self._check("3d12 | cn:>6 + 1", min_result=1, max_result=4)

    def test_res_cn_menos_inteiro(self):
        # cn:8..10 em 2d10 → 0..2, -5 → -5..-3
        self._check("2d10 | cn:8..10 - 5", min_result=-5, max_result=-3)

    # ── Encadeamentos duplos ──────────────────────────────────────────────────

    def test_res_kh_cn(self):
        # kh:2 de 4d6 → pool de 2 dados; cn conta 6s → 0..2
        self._check("4d6 | kh:2 | cn:6", min_result=0, max_result=2)

    def test_res_kh_ex(self):
        self._check("4d6 | kh:2 | ex:>5", min_result=2)

    def test_res_kh_rr(self):
        self._check("4d6 | kh:2 | rr:1", min_result=2, max_result=12)

    def test_res_kl_cn(self):
        self._check("4d6 | kl:2 | cn:1", min_result=0, max_result=2)

    def test_res_kl_ex(self):
        self._check("4d6 | kl:2 | ex:<2", min_result=2)

    def test_res_kl_rr(self):
        self._check("4d6 | kl:2 | rr:1", min_result=2, max_result=12)

    def test_res_ex_cn(self):
        self._check("3d6 | ex:6 | cn:6", min_result=0, max_result=6)

    def test_res_ex_kh(self):
        self._check("3d6 | ex:6 | kh:2", min_result=2)

    def test_res_ex_kl(self):
        self._check("3d6 | ex:6 | kl:1", min_result=1)

    def test_res_ex_rr(self):
        self._check("3d6 | ex:6 | rr:1", min_result=3)

    def test_res_rr_cn(self):
        self._check("3d6 | rr:1 | cn:>3", min_result=0, max_result=3)

    def test_res_rr_kh(self):
        self._check("3d6 | rr:1 | kh:2", min_result=2, max_result=12)

    def test_res_rr_kl(self):
        self._check("3d6 | rr:1 | kl:1", min_result=1, max_result=6)

    def test_res_rr_ex(self):
        self._check("3d6 | rr:1 | ex:6", min_result=3)

    # ── Encadeamentos triplos ─────────────────────────────────────────────────

    def test_res_kh_ex_cn(self):
        # kh:3 de 4d6 → 3 dados; ex:6 pode adicionar mais; cn conta 6s
        self._check("4d6 | kh:3 | ex:6 | cn:6", min_result=0)

    def test_res_kh_rr_cn(self):
        self._check("4d6 | kh:3 | rr:1 | cn:>4", min_result=0, max_result=3)

    def test_res_ex_kh_cn(self):
        self._check("4d6 | ex:6 | kh:3 | cn:6", min_result=0, max_result=3)

    def test_res_rr_kh_cn(self):
        self._check("4d6 | rr:1 | kh:3 | cn:>4", min_result=0, max_result=3)

    # ── Operadores com múltiplos dados e funções ──────────────────────────────

    def test_res_kl_mais_kh(self):
        # kl:2 de 4d6 → 2..12; kh:4 de 5d10 → 4..40 → total 6..52
        self._check("4d6 | kl:2 + 5d10 | kh:4", min_result=6, max_result=52)

    def test_res_rr_mais_ex(self):
        self._check("3d6 | rr:1 + 1d10 | ex:10", min_result=4)

    # ── mr ───────────────────────────────────────────────────────────────────

    def test_res_mr_e_lista(self):
        self._check("2d6 | mr:3", is_list=True, list_len=3)

    def test_res_mr_itens_no_intervalo(self):
        ok, result, _ = run("2d6 | mr:4")
        self.assertTrue(ok)
        for v in result:
            self.assertGreaterEqual(v, 2)
            self.assertLessEqual(v, 12)

    def test_res_mr_log_contem_rolls(self):
        self._check("d20 | mr:4", is_list=True, list_len=4,
                    log_contains=["4x rolls", "[1]", "[4]"])

    def test_res_mr_com_kh(self):
        # D&D: 4d6|kh:3 repetido 6 vezes → lista de 6 ints em 3..18
        ok, result, log = run("4d6 | kh:3 | mr:6")
        self.assertTrue(ok)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 6)
        for v in result:
            self.assertGreaterEqual(v, 3)
            self.assertLessEqual(v, 18)
        self.assertIn("Keep", log)

    def test_res_mr_com_rr(self):
        self._check("3d6 | rr:1 | mr:3", is_list=True, list_len=3)

    def test_res_mr_com_ex(self):
        ok, result, _ = run("2d8 | ex:>7 | mr:4")
        self.assertTrue(ok)
        self.assertEqual(len(result), 4)
        for v in result:
            self.assertGreaterEqual(v, 2)

    def test_res_mr_com_cn(self):
        ok, result, _ = run("3d6 | cn:>4 | mr:3")
        self.assertTrue(ok)
        self.assertEqual(len(result), 3)
        for v in result:
            self.assertGreaterEqual(v, 0)
            self.assertLessEqual(v, 3)

    def test_res_mr_soma_inteiro(self):
        # 5d6 + 1 → 6..31; mr:2 → lista de 2
        ok, result, _ = run("5d6 + 1 | mr:2")
        self.assertTrue(ok)
        self.assertEqual(len(result), 2)
        for v in result:
            self.assertGreaterEqual(v, 6)
            self.assertLessEqual(v, 31)

    def test_res_mr_kh_soma_inteiro(self):
        # 4d6|kh:3 → 3..18, +2 → 5..20; mr:3 → lista de 3
        ok, result, _ = run("4d6 | kh:3 + 2 | mr:3")
        self.assertTrue(ok)
        self.assertEqual(len(result), 3)
        for v in result:
            self.assertGreaterEqual(v, 5)
            self.assertLessEqual(v, 20)

    def test_res_mr_menos_inteiro(self):
        # 3d6 → 3..18, -1 → 2..17; mr:4 → lista de 4
        ok, result, _ = run("3d6 - 1 | mr:4")
        self.assertTrue(ok)
        self.assertEqual(len(result), 4)
        for v in result:
            self.assertGreaterEqual(v, 2)
            self.assertLessEqual(v, 17)


# ─────────────────────────────────────────────────────────────────────────────
# Runner
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()

    # Ordem: parser válido → parser inválido → resolução
    for cls in (TestParserValid, TestParserInvalid, TestResolution):
        suite.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)