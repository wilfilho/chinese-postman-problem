# Chinese Postman Problem

## Links Importantes

- [Apresentação do Carteiro Chinês por Wilson e Ian](https://www.youtube.com/watch?v=NWDg1k07rX4)
- [Slide da Apresentação do Carteiro Chinês](https://docs.google.com/presentation/d/1QvCC7OJI2UqHbjNPdNmWlFaHlQXK0JwV7SlUYAApEPc/edit?usp=sharing)

## Autores

- Ian Sandes Alves
- José Wilson Martins Filho

## Descrição

Esta implementação resolve o **Problema do Carteiro Chinês** (Chinese Postman Problem), um problema de teoria dos grafos que busca encontrar o menor caminho fechado que visita todas as arestas de um grafo pelo menos uma vez.

## Funcionalidades

### Algoritmos Implementados

- **Algoritmo de Dijkstra**: Calcula caminhos mínimos entre vértices
- **Algoritmo de Hierholzer**: Encontra circuitos eulerianos em grafos
- **Programação Dinâmica com Bitmask**: Resolve o problema de emparelhamento mínimo
- **Solução Completa do Chinese Postman**: Integra todos os algoritmos para resolver o problema

### Estrutura do Código

#### Funções Principais

1. **`build_adjacency_list(edges_list)`**
   - Constrói lista de adjacência a partir de lista de arestas
   - Entrada: Lista de tuplas `(origem, destino, nome da aresta)`
   - Saída: Dicionário com lista de adjacência

2. **`dijkstra(adjacency_list, source_vertex)`**
   - Implementa algoritmo de Dijkstra para caminhos mínimos
   - Retorna distâncias e predecessores para reconstrução de caminhos

3. **`hierholzer(adjacency_list, starting_vertex)`**
   - Encontra circuito euleriano usando algoritmo de Hierholzer
   - Funciona apenas em grafos eulerianos

4. **`chinese_postman_problem(edges_list, starting_vertex="V1")`**
   - Função principal que resolve o problema do carteiro chinês
   - Retorna custo total e tour completo

## Como Usar

### Exemplo Básico

```python
from chinese_postman import chinese_postman_problem, graph_edges

# Executar com o grafo padrão
resultado = chinese_postman_problem(graph_edges, starting_vertex="V1")

print(f"Custo total: {resultado['total_cost']}")
print(f"Tour: {resultado['tour']}")
```

### Definindo Seu Próprio Grafo

```python
# Definir arestas como lista de tuplas (origem, destino, nome da aresta)
minhas_arestas = [
    ("A", "B", "e1"),
    ("B", "C", "e2"),
    ("C", "A", "e3")
]

resultado = chinese_postman_problem(minhas_arestas, starting_vertex="A")
```

## Estrutura do Resultado

A função retorna um dicionário com:

- **`total_cost`**: Custo total do tour (número de arestas atravessadas)
- **`tour`**: Sequência de vértices do tour completo

## Complexidade

- **Tempo**: O(V³ + E·V + 2^k · k²), onde k é o número de vértices de grau ímpar
- **Espaço**: O(V² + E + 2^k) para armazenar distâncias e cache de programação dinâmica

## Dependências

- `collections.defaultdict`: Para estruturas de dados eficientes
- `heapq`: Para implementação da fila de prioridade no Dijkstra
- `functools.lru_cache`: Para memoização na programação dinâmica

## Grafo de Exemplo

O código inclui um grafo predefinido com 25 vértices (V1 a V25) e 35 arestas, representando uma rede complexa para demonstração.

## Limitações

- O algoritmo assume que todas as arestas têm peso unitário (1)
- O grafo deve ser conexo para ter uma solução válida
- A complexidade exponencial limita o uso para grafos com muitos vértices de grau ímpar
