import unittest
from FlightsGraph import AirportVertex, FlightsGraph

class TestShortestPath(unittest.TestCase):


    def test_shortest_path(self):
    
        airport_BOS = AirportVertex('BOS')
        airport_JFK = AirportVertex('JFK')
        airport_CLT = AirportVertex('CLT')
        airport_ORD = AirportVertex('ORD')
        airport_ATL = AirportVertex('ATL')
        airport_DFW = AirportVertex('DFW')
        airport_DEN = AirportVertex('DEN')
        airport_LAS = AirportVertex('LAS')
        airport_LAX = AirportVertex('LAX')
        airport_SFO = AirportVertex('SFO')
        airport_SEA = AirportVertex('SEA')

        graph = FlightsGraph(False)

        graph.add_vertex(airport_BOS.get_id())
        graph.add_vertex(airport_JFK.get_id())
        graph.add_vertex(airport_CLT.get_id())
        graph.add_vertex(airport_ORD.get_id())
        graph.add_vertex(airport_ATL.get_id())
        graph.add_vertex(airport_DFW.get_id())
        graph.add_vertex(airport_DEN.get_id())
        graph.add_vertex(airport_LAS.get_id())
        graph.add_vertex(airport_LAX.get_id())
        graph.add_vertex(airport_SFO.get_id())
        graph.add_vertex(airport_SEA.get_id())



        graph.add_edge(airport_SEA.get_id(), airport_SFO.get_id(), 5)
        graph.add_edge(airport_SFO.get_id(), airport_LAX.get_id(), 5)
        graph.add_edge(airport_LAX.get_id(), airport_LAS.get_id(), 5)
        graph.add_edge(airport_SFO.get_id(), airport_LAS.get_id(), 8)
        graph.add_edge(airport_LAS.get_id(), airport_DEN.get_id(), 2)
        graph.add_edge(airport_DEN.get_id(), airport_ORD.get_id(), 5)
        graph.add_edge(airport_ORD.get_id(), airport_JFK.get_id(), 10)
        graph.add_edge(airport_JFK.get_id(), airport_BOS.get_id(), 2)
        graph.add_edge(airport_JFK.get_id(), airport_CLT.get_id(), 3)
        graph.add_edge(airport_DFW.get_id(), airport_ORD.get_id(), 15)
        graph.add_edge(airport_DFW.get_id(), airport_ATL.get_id(), 10)
        graph.add_edge(airport_ATL.get_id(), airport_JFK.get_id(), 30)
        graph.add_edge(airport_BOS.get_id(), airport_ATL.get_id(), 15)
        graph.add_edge(airport_BOS.get_id(), airport_SFO.get_id(), 50)

        self.assertEqual(27, graph.find_shortest_path('BOS', 'SFO'))

