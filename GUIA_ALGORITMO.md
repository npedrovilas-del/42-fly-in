# Guia: vários caminhos no Fly-in

Objetivo: em vez de todos os drones seguirem o mesmo caminho em fila, usar 2 ou mais caminhos quando isso compensa.
Faz um passo de cada vez e só avanças quando todos os mapas continuarem a dar os mesmos turnos que antes (ou menos).

---

## Passo 0: rede de segurança (15 min)
- Guarda os benchmarks atuais: linear 4, fork 6, basic 4, dead_end 8, circular 15, priority 8, maze 13, capacity_hell 16, ultimate 26, impossible 91.
- Muda a condição de fim para "TODOS os drones chegaram" (e não "o drone 1 chegou").
- Pergunta: como sabes, num turno, que todos os drones estão no `end`?

## Passo 1: cada drone com o seu caminho (30 min)
- Hoje o `run` usa o `path` global. Passa a usar `drone.path` em todo o lado.
- Ainda dás o MESMO caminho a todos. O resultado tem de ser igual ao de antes.
- Pergunta: em que sítios do `move_drones` usas `path` em vez de `drone.path`?

## Passo 2: um segundo caminho (1 h)
- Ideia: corre o Dijkstra outra vez, mas "proíbe" as zonas do meio do 1.º caminho (não o start nem o end).
- Pergunta: o teu `dijkstra` consegue receber um conjunto de zonas a ignorar? Onde é que ele decide se visita um vizinho?
- Testa no `fork` e no `capacity_hell`: imprime os dois caminhos e vê se fazem sentido.
- Se não houver 2.º caminho (devolve inf), usa só o 1.º.

## Passo 3: dividir os drones (1 h)
- Um caminho de custo C com N drones demora mais ou menos C + (N - 1) turnos, porque sai 1 drone por turno.
  Com capacidade maior, divide esse (N - 1) pela capacidade.
- Ideia simples (gulosa): para cada drone, escolhe o caminho onde ele ACABA mais cedo:
  `custo_do_caminho + drones_já_nesse_caminho`.
- Pergunta: se o caminho A tem custo 5 e o B custo 8, para onde vão os 4 primeiros drones?
  (Resposta: os 3 primeiros para o A, e o 4.º empata, 5+3 = 8+0.)

## Passo 4: testar e comparar (30 min)
- Corre todos os mapas. Se algum PIORAR, há duas causas comuns:
  1. O 2.º caminho passa pelo mesmo bottleneck (ex.: `final_bottleneck` no capacity_hell). Dividir não ajuda nada aí.
  2. Os drones bloqueiam-se uns aos outros num cruzamento.
- Plano B: se piorar num mapa, usa só 1 caminho nesse mapa (calcula as duas versões e fica com a melhor).

## Passo 5 (opcional): o impossible
- O mínimo teórico é 43, e o recorde é 45.
- O 1.º drone vai pelo atalho de emergência (19 turnos), e depois só passa 1 drone por turno nos gargalos de capacidade 1.
- Pergunta: o teu Dijkstra está a escolher esse atalho? Imprime o caminho e compara.

---

### Quando estiveres preso
Diz-me em que passo estás e o que acontece (o output ou o erro). Eu dou-te uma pista, não a solução.
