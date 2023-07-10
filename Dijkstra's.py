import heapq

def getShortestPath(G,source,destination): #djikstras...
  queue = [] ; visited = []
  cost = {} ; route=[] ; temp = []
  d=destination
  for node in G:
    cost[node] = float('inf')
  cost[source] = 0
  heapq.heappush(queue,(cost[source],source)) 
  while queue:
    p = heapq.heappop(queue) # p[0] is cost ; p[1] is node
    if p[1] not in visited:
      visited.append(p[1])
      for label in G[p[1]]: # label[0] is node ; label[1] is cost
        if label[0] not in visited:
          new_cost = cost[p[1]] + label[1]
          if new_cost < cost[label[0]]:
            temp.append((p[1],label[0])) # routes, need to 'sort' them later from destination to source.
            cost[label[0]] = new_cost
          heapq.heappush(queue,(cost[label[0]],label[0]))
  for something in temp[::-1]:
    if something[1]==d:
      route.append(something)
      d=something[0]
  return route[::-1]