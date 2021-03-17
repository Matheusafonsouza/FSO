Gramáticas livres de contexto
=============================


## [cfg-bnf]: Entender e reconhecer operações básicas de gramática generativa na notação BNF

Expresse as linguagens abaixo em notação BNF (não utilize os operadores extendidos (*, +, [], ?, ()))

1. Uma ou mais ocorrências de a. Ex.: `a, aaa, aaaaaaa`
2. Strings que começam com a, seguem com uma ou mais ocorrências de b ou c e terminam com d. Ex.: `ad, abcd, abbbd`
3. Números positivos com parte decimal opcional. Ex.: `0, 42, 3.14`


## [cfg-ebnf]: Entender operadores na notação EBNF

Converta as expressões em EBNF para BNF assumindo que os símbolos terminais e não-terminais utilizados estão definidos adequadamente fora da regra em questão.

1. `imp : "from" name "import" (VAR [as VAR])+`
2. `seq : "(" (a | b)* ")"`
3. `lst : "{" [key ":" exp ("," key ":" exp)* ","?] "}"`


## [cfg-list]: Representar sequências em notação BNF e EBNF

Resolva uma das questões abaixo para obter a competência. 

**Q1)** Monte uma gramática BNF ou EBNF para identificar listas de elementos em cada um dos casos abaixo:

1. JSON: usa "[]" como delimitadores e exige uma vírgula entre cada elemento da lista
2. LISP: usa "()" como delimitadores e não utiliza vírgulas para separar os elementos.
3. LISP-II: em algumas versões de LISP, a vírgula é opcional, também podendo aparecer após o último elemento.
4. Python: similar ao JSON, mas permite uma vírgula após o último elemento. `[,]` é inválido.
5. Javascript: similar ao JSON, mas aceita **1 ou mais** vírgulas entre os elementos e após o último elemento. `[,]`, assim como `[1,2,,3,,,]` são valores válidos. Em Javascript, o espaço vazio entre duas vírgulas é interpretado como um elemento `undefined`.

Assuma que uma regra para produção de elementos (elem) esteja definida em algum lugar da gramática.

**Q2)** Crie um programa baseado no último exemplo da questão anterior que leia listas no estilo Javascript e retorne o valor processado, trocando `undefined` por None em Python. Assuma que os elementos podem ser outras listas ou números inteiros. Deste modo, o código de entrada `"[1,,2,[,,],]"` seria convertido em `[1, None, 2, [None, None]]`.


## [cfg-op]: Representar precedência de operadores em gramática (E)BNF

**Q1)** Algumas linguagens de programação possuem operadores de composição e aplicação de funções. Por exemplo, em Elm e F#, a expressão `x |> f` significa executar a função `f` com o argumento `x`. Este operador é associativo à esquerda `x |> f |> g = (x |> f) |> g`. Já `f >> g` cria uma nova função que passa o argumento para f e o resultado disto para g. Este operador também é associativo à esquerda e possui uma precedência maior que `|>`, de forma que `x |> f >> g >> h |> w` pode ser interpretado como `(x |> ((f >> g) >> h)) |> w`.

Crie uma gramática para uma mini linguagem que inclua estes operadores e nomes como `x`, `y`, `f`, `g`, etc como símbolos terminais. Certifique-se que a gramática proposta obedece às leis de associatividade e precedência descritas acima. 


## [cfg-cst]: Relacionar gramática com a representação do código como árvore concreta 

**Q1)** A árvore sintática concreta representa um determinado elemento de uma linguagem como uma árvore que inclui **todos** lexemas como folhas e, deste modo, apresenta uma descrição 1:1 entre o código de entrada e a representação estruturada do mesmo. Usando a gramática abaixo, desenhe uma representação como árvore sintática completa das seguintes expressões:

1. 42
2. 2 * (11 + 2 * 5)

```
expr : expr "+" term
     | term

term : term "*" atom
     | atom

atom : NUMBER
     | "(" expr ")"

NUMBER : /\d+/
```

## [cfg-ast]: Criar árvore sintática 

**Q1)** Utilize a linguagem definida pela gramática da questão "cfg-cst.Q1" para criar uma classe Transformer que converta o código em uma representação formada por números ou dicionários como nos exemplos.

```python
... # Cria o transformer


def ast(x):
    return transformer.transform(grammar.parse(src))

assert ast("42") == 42
assert ast("1 + 1") == {"op": "+", "left": 1, "right": 1} 
assert ast("1 + 2 * 3") == {"op": "+", "left": 1, "right": {"op": "*", "left": 2, "right": 3}}
```

## [cfg-sexpr]: Dominar a representação de árvores sintáticas abstratas por S-Expressions

**Q1)** Utilize a linguagem definida pela gramática da questão "cfg-cst.Q1" para criar uma classe Transformer que converta o código em uma representação formada por listas com a representação prefixa da operação como nos exemplos abaixo.

```python
... # Cria o transformer


def ast(x):
    return transformer.transform(grammar.parse(src))

assert ast("42") == 42
assert ast("1 + 1") == ["+", 1, 1]
assert ast("1 + 2 * 3") == ["+", 1, ["*", 2, 3]]
```

Este tipo de representação é utilizado em LISP e recebeu o nome de expressões-S.


## [cfg-reduce]: Utilizar transformers para obter resultados a partir da análise sintática 

**Q1)** Crie um programa que lê árvores sintáticas abstratas no formato produzido por "cfg-ast.Q1" ou "cfg-sexpr.Q1" (escolha um dos dois) e avalie o resultado da expressão matemática.

```python

def calc(x):
    return transformer.transform(grammar.parse(src))

assert calc(42) == 42
assert calc(["+", 1, 1]) == 2  # Se preferir, utilize a representação como dicionários!
assert calc(["+", 1, ["*", 2, 3]]) == 6
```