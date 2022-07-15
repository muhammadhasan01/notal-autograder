import os.path
import unittest

from grader.src.cfggenerator.cfggenerator import PythonCfgGenerator
from grader.src.ged.classes.general_cost_function import GeneralCostFunction, RelabelMethod
from grader.src.ged.dfs_ged import DFSGED
from grader.src.grader import Grader, GraphPreprocessType


class DFSGEDTest(unittest.TestCase):
    EPS = 1e-5
    REF_SOL = {
        'segiempat': {
            'references': ['segiempat_ref.py'],
            'solutions': ['segiempat1.py', 'segiempat2.py']
        }
    }

    def get_source(self, filename):
        filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', filename)
        with open(filename, 'r', encoding='UTF-8') as file:
            raw_code = file.read()
            return raw_code

    def test_compute_edit_distance_valid(self):
        general_cost_function = GeneralCostFunction(relabel_method=RelabelMethod.BOOLEAN_COUNT)

        cfggenerator = PythonCfgGenerator()
        references = [cfggenerator.generate_python(self.get_source(filename)) for filename in self.REF_SOL['segiempat']['references']]
        solutions = [cfggenerator.generate_python(self.get_source(filename)) for filename in self.REF_SOL['segiempat']['solutions']]

        grader = Grader()
        for solution in solutions:
            for reference in references:
                dfs_ged = DFSGED(grader.preprocess_graph(solution, GraphPreprocessType.PROPAGATE_BRANCHING),
                                grader.preprocess_graph(reference, GraphPreprocessType.PROPAGATE_BRANCHING),
                                general_cost_function)
                dfs_ged.compute_edit_distance(is_exact_computation=True)
                assert(dfs_ged.is_valid_exact_computation())

    def test_cost_function_precompute(self):
        general_cost_function1 = GeneralCostFunction(relabel_method=RelabelMethod.BOOLEAN_COUNT)
        general_cost_function2 = GeneralCostFunction(relabel_method=RelabelMethod.BOOLEAN_COUNT)

        cfggenerator = PythonCfgGenerator()
        references = [cfggenerator.generate_python(self.get_source(filename)) for filename in self.REF_SOL['segiempat']['references']]
        solutions = [cfggenerator.generate_python(self.get_source(filename)) for filename in self.REF_SOL['segiempat']['solutions']]

        grader = Grader()
        for solution in solutions:
            for reference in references:
                source = grader.preprocess_graph(solution, GraphPreprocessType.PROPAGATE_BRANCHING)
                target = grader.preprocess_graph(reference, GraphPreprocessType.PROPAGATE_BRANCHING)
                dfs_ged1 = DFSGED(source,
                                target,
                                general_cost_function1)
                dfs_ged1.compute_edit_distance(is_exact_computation=False)

                dfs_ged2 = DFSGED(source,
                                target,
                                general_cost_function2)
                dfs_ged2.cost_function.do_node_precompute = False
                dfs_ged2.compute_edit_distance(is_exact_computation=False)

                for node1 in source.nodes:
                    for node2 in target.nodes:
                        assert(abs(general_cost_function1.get_node_cost(node1, node2) -
                                   general_cost_function2.get_node_cost(node1, node2)) <= self.EPS)
