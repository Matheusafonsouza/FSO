"""
COMPETÊNCIA [cfg-classicas]: 

    Montar e reconhecer gramáticas livres de contexto para exemplos clássicos de 
    linguagens simples 


BASEADO NO EXERCÍCIO:

    Crie gramáticas livres de contexto (utilizndo o Lark ou simplesmente a 
    sintaxe EBNF) que identifiquem as seguintes linguagens:

    1. Strings formadas por n a's seguidas de n b's; n >= 1. Ex.: `aabb, ab, aaabbb`.
    2. Letras L Dentro de parênteses pareados. Ex.: `LL, (LL), L(L(LL)), (((L)))`
    3. Listas com elementos separados por vírgulas. Ex.: `[], [e], [e,e,e]`
    4. Listas que podem conter outras listas. Ex.: `[], [[]], [e], [e,[e,[]],e]`
    5. Expressões matemáticas no estilo prefixo. Ex.: `42, + 1 2, + * 10 2 2`


BACKLOG:

    - Reaproveitar este código para correção de outros exercícios baseados no
      Lark
    - Montar mecanismos para criação automática de exemplos e testadores a
      partir do gabarito.


COMPETÊNCIAS ADICIONAIS:

    [code-golf*]:
        Implemente versões **CORRETAS** das funções mk() ou check() de alguma
        das classes abaixo utilizando um número menor de tokens que as utilizadas
        neste módulo.

    [bug-hunter*]:
        Encontre uma falha lógica nestes testes. Normalmente o bug se enquadra
        em uma das categorias abaixo:
        
        1. testes aceitam uma gramática incorreta.
        2. testes recusam uma gramática correta.
        3. função mk() não consegue produzir alguns exemplos corretos.
        4. a função mk() pode produzir exemplos incorretos.

    [monitor*]:
        Implemente um exercício adicional como os outros deste módulo para 
        alguma outra gramática clássica. Bons exemplos incluem operadores
        pósfixos/infixos, algumas variações de representações de listas 
        (aceita ou não vírgula final, aceita vírgulas intermediárias, etc) 
        entre outros. 
"""

from lark import Lark, LarkError
from collections import deque
from types import SimpleNamespace
from random import random, randint, randrange, choice
from typing import Callable
import pytest
from pathlib import Path
import os

PATH = Path(__file__).parent
MUTATORS = []

is_mutator = MUTATORS.append


@is_mutator
def reverse(tks):
    tks.reverse()


@is_mutator
def insert_random(tks):
    if tks:
        tks.insert(randrange(len(tks)), choice(tks))


@is_mutator
def delete_random(tks):
    if tks:
        del tks[randrange(len(tks))]


@is_mutator
def swap_random(tks):
    if tks:
        i = randrange(len(tks))
        j = randrange(len(tks))
        tks[i], tks[j] = tks[j], tks[i]


class Grammar:
    mk: Callable
    check: Callable
    name: str
    BAD_EXAMPLES = ()
    GOOD_EXAMPLES = ()

    @pytest.fixture(scope="class")
    def mod(self):
        paths = ["respostas.py", "gabarito.py"]
        if os.environ.get('GABARITO', 'false').lower() in ('true', 't'):
            paths.reverse()        

        for f in paths:
            if (PATH / f).exists():
                src = (PATH / f).read_text()
                ns = {}
                exec(src, ns)
                return SimpleNamespace(**ns)

        raise RuntimeError("módulo respostas.py não existe")

    @pytest.fixture
    def grammar(self, mod, parser_method):
        src = getattr(mod, self.name).strip()
        if not src or src == 'start : "..."':
            pytest.skip("Gramática vazia")
        return Lark(src)

    @pytest.fixture(params=['lalr', 'earley'])
    def parser_method(self, request):
        return request.param

    def good(self):
        yield from self.GOOD_EXAMPLES

        for _ in range(100 - len(self.GOOD_EXAMPLES)):
            yield self.mk()

    def bad(self):
        yield from self.BAD_EXAMPLES
        n = len(self.BAD_EXAMPLES)

        for _ in range(5000):
            if n >= 250:
                return

            bad = list(self.mk())
            for _ in range(5):
                self.corrupt(bad)
                src = "".join(bad)
                if random() < 0.5 and not self.is_good(src):
                    n += 1
                    yield "".join(bad)
                    break

        raise RuntimeError(f"só conseguiu gerar {n} exemplos ruins")

    def is_good(self, src):
        try:
            self.check(src)
            return True
        except (IndexError, AssertionError):
            return False

    def corrupt(self, src):
        return choice(MUTATORS)(src)

    def test_mk_check_funcionam_corretamente(self):
        # (Este é apenas um teste interno)
        mk, check = self.mk, self.check
        for _ in range(100):
            batch = [mk() for _ in range(10)]
            for x in batch:
                try:
                    check(x)
                except (AssertionError, IndexError):
                    print(f"Exemplo errado: {x}")
                    raise

    def test_gramática_aceita_valores_corretos(self, grammar):
        for ex in self.good():
            grammar.parse(ex)

    def test_gramática_recusa_erros(self, grammar):
        for ex in self.bad():
            with pytest.raises(LarkError):
                grammar.parse(ex)
                print(f'Exemplo inválido foi aceito: {ex}')


class TestStringsPareadas(Grammar):
    """
    Strings formadas por n a's seguidas de n b's; n >= 1.

    Ex.: `aabb, ab, aaabbb`.
    """

    name = "strings_pareadas"

    def mk(self, d=6):
        if d <= 0 or random() < 0.75:
            return "ab"
        return f"a{self.mk(d - 1)}b"

    def check(self, st):
        As, sep, Bs = st.partition("b")
        if sep:
            Bs += "b"
        assert set(As) == {"a"} and set(Bs) == {"b"} and len(As) == len(Bs)


class TestLetrasDentroDeParênteses(Grammar):
    """
    Letras L Dentro de parênteses pareados.

    Ex.: `LL, (LL), L(L(LL)), (((L)(L)))`
    """

    name = "letras_dentro_de_parenteses"

    def mk(self, d=3):
        if d <= 0 or random() < 0.5:
            return "L" * randint(1, 4)
        if random() < 0.25:
            return "".join(self.mk(d - 1) for _ in range(randint(1, 4)))
        items = "".join(self.mk(d - 1) for _ in range(randint(1, 4)))
        return f"({items})"

    def check(self, st):
        assert st
        tks = deque(st.replace("L", ""))
        assert not tks or set(tks) == set("()")

        def expr():
            if tks:
                assert tks.popleft() == "("
                while tks[0] == "(":
                    expr()
                tks.popleft() == ")"

        while tks:
            expr()


class TestListasComElementosSeparadosPorVírgulas(Grammar):
    """
    Listas com elementos separados por vírgulas.

    Ex.: `[], [e], [e,e,e]`
    """

    name = "listas_com_elementos_separados_por_virgulas"

    def mk(self):
        data = ",".join("e" for _ in range(randint(0, 10)))
        return f"[{data}]"

    def check(self, st):
        assert st[0] == "[" and st[-1] == "]"
        assert len(st) == 2 or set(st[1:-1].split(",")) == {"e"}


class TestListasAninhadas(Grammar):
    """
    Elementos e listas que podem conter outras listas.

    Ex.: `e, [], [[]], [e], [e,[e,[]],e]`
    """

    name = "listas_aninhadas"

    def mk(self, d=5):
        if d <= 0 or random() < 0.5:
            return "e"
        data = ",".join(self.mk(d - 1) for _ in range(randint(0, 7)))
        return f"[{data}]"

    def check(self, st):
        tks = deque(st)
        assert set(tks).issubset("[]e,")

        def expr():
            c = tks.popleft()
            if c == "[":
                if tks[0] != "]":
                    args()
                assert tks.popleft() == "]"
            else:
                assert c == "e"

        def args():
            expr()
            while tks[0] == ",":
                tks.popleft()
                expr()

        expr()
        assert not tks


class TestOperadoresPrefixos(Grammar):
    """
    Expressões matemáticas no estilo prefixo.

    Ex.: `42, + 1 2, + * 10 2 2`
    """

    ops = list("+*-/^")
    name = "operadores_prefixos"

    def mk(self, d=5):
        if d <= 0 or random() < 0.5:
            return str(randint(0, 1000))
        return f"{choice(self.ops)} {self.mk(d - 1)} {self.mk(d - 1)}"

    def check(self, st):
        tks = deque(st.split())

        def expr():
            tk = tks.popleft()
            if tk in self.ops:
                expr()
                expr()
            else:
                assert tk.isdigit()

        expr()
        assert not tks