from util import make_arg_simple
from datatypes.Operand import Operand
from annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer
from annotation_generation.datatypes.parallelizability.Aggregator import Aggregator

import annotation_generation.AnnotationGeneration as AnnotationGeneration

cmd_name = "tr"

# commands taken from spell script in one-liners


def test_tr_1() -> None:
    args = [make_arg_simple(["-c"]), make_arg_simple(["-s"])]
    operands = [Operand("A-Za-z"),
                Operand("\'\n\'")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 1
    assert len(meta.get_output_list()) == 2     # stdout and stderr

    assert len(meta.get_parallelizer_list()) == 1
    [parallelizer1] = meta.get_parallelizer_list()
    assert parallelizer1 == Parallelizer.make_parallelizer_round_robin()


def test_tr_2() -> None:
    args = []
    operands = [Operand("A-Z"),
                Operand("a-z")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 1
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 1
    [parallelizer1] = meta.get_parallelizer_list()
    assert parallelizer1 == Parallelizer.make_parallelizer_round_robin()


def test_tr_3() -> None:
    args = [make_arg_simple(["-d"])]
    operands = [Operand("'[:punct:]'")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 1
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 1
    [parallelizer1] = meta.get_parallelizer_list()
    assert parallelizer1 == Parallelizer.make_parallelizer_round_robin()


def test_tr_4() -> None:
    args = [make_arg_simple(["-d"])]
    operands = [Operand("'\n'")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 1
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 1
    [parallelizer1] = meta.get_parallelizer_list()
    assert parallelizer1 == Parallelizer.make_parallelizer_round_robin()


def test_tr_5() -> None:
    args = [make_arg_simple(["-c"]), make_arg_simple(["-d"])]
    operands = [Operand("'\n'")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 1
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 1
    [parallelizer1] = meta.get_parallelizer_list()
    assert parallelizer1 == Parallelizer.make_parallelizer_round_robin()


def test_tr_6() -> None:
    args = [make_arg_simple(["-c"]), make_arg_simple(["-d"])]
    operands = [Operand("A-Z")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 1
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 1
    [parallelizer1] = meta.get_parallelizer_list()
    assert parallelizer1 == Parallelizer.make_parallelizer_round_robin()
