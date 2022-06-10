from __future__ import annotations
from typing import Optional, List, Literal

from abc import ABC, abstractmethod

from util_standard import standard_repr, standard_eq

from datatypes_new.CommandInvocationWithIO import CommandInvocationWithIO
from datatypes_new.BasicDatatypes import FileNameOrStdDescriptor
from annotation_generation_new.datatypes.parallelizability.TransformerFlagOptionList import TransformerFlagOptionList
# from annotation_generation_new.datatypes.parallelizability.TransformerPosConfigList import TransformerPosConfigList
from annotation_generation_new.datatypes.parallelizability.AggregatorKind import AggregatorKindEnum
from annotation_generation_new.datatypes.parallelizability.Aggregator import Aggregator
from util_new import return_default_if_none_else_itself

# What spec needs to contain for which one:

# CONCATENATE:      only kind
# ADJ_LINES_MERGE:  only kind
# ADJ_LINES_SEQ:    only kind, return can be computed from parameters

# ADJ_LINES_FUNC:   function for adjacent lines (2 inputs)
# CUSTOM_2_ARY:     function for two blocks     (2 inputs)
# could be given as transformation of original command or parsed from string representation

# CUSTOM_N_ARY:     function for all blocks     (multiple inputs)
# as for 2 inputs but some way to specify additional inputs,
# hard-coded appended to operand list? currently no use case anyway...

class AggregatorSpec(ABC):

    def __init__(self,
                 kind: AggregatorKindEnum,
                 # spec_agg_cmd_name: str,
                 # for now, we keep everything in operand list as it is but substitute streaming input and output
                 is_implemented: bool = False
                 ) -> None:
        self.kind: AggregatorKindEnum = kind
        # self.spec_agg_cmd_name: str = spec_agg_cmd_name # for the rest, it should be specified
        # self.flag_option_list_transformer: TransformerFlagOptionList = \
        #     TransformerFlagOptionList.return_transformer_empty_if_none_else_itself(flag_option_list_transformer)
        self.is_implemented = is_implemented


    def __eq__(self, other: AggregatorSpec) -> bool:
        return standard_eq(self, other)

    def __repr__(self) -> str:
        return standard_repr(self)

    # Spec shall be hold by PaSh and once needed, gets actual aggregator from this function
    # return value None if it is not yet implemented
    # PaSh ought to provide the correct input based on the kind of aggregator, e.g., line
    # for CONCATENATE and CUSTOM_N_ARY, we need to provide the number of inputs to give back
    @abstractmethod
    def get_aggregator(self,
                       original_cmd_invocation: CommandInvocationWithIO,
                       inputs_from: List[FileNameOrStdDescriptor],
                       output_to: FileNameOrStdDescriptor
                       ) -> Optional[Aggregator]:
        pass

    @staticmethod
    def make_aggregator_spec_concatenate() -> AggregatorSpec:
        return AggregatorSpecNonFunc(AggregatorKindEnum.CONCATENATE, is_implemented=True)

    @staticmethod
    def make_aggregator_spec_adj_lines_merge() -> AggregatorSpec:
        return AggregatorSpecNonFunc(AggregatorKindEnum.ADJ_LINES_MERGE, is_implemented=False)

    @staticmethod
    def make_aggregator_spec_adj_lines_seq() -> AggregatorSpec:
        return AggregatorSpecNonFunc(AggregatorKindEnum.ADJ_LINES_SEQ, is_implemented=False)

    @staticmethod
    def make_aggregator_spec_adj_lines_func_from_cmd_inv_with_transformers(
            flag_option_list_transformer: Optional[TransformerFlagOptionList] = None,
            # pos_config_list_transformer: Optional[TransformerPosConfigList] = None,
            is_implemented: bool = False) -> AggregatorSpec:
        return AggregatorSpecFuncTransformer(kind=AggregatorKindEnum.ADJ_LINES_FUNC,
                                             flag_option_list_transformer=flag_option_list_transformer,
                                             # pos_config_list_transformer=pos_config_list_transformer,
                                             is_implemented=is_implemented)

    @staticmethod
    def make_aggregator_spec_adj_lines_func_from_string_representation(
            cmd_inv_as_str: str,
            is_implemented: bool= False) -> AggregatorSpec:
        return AggregatorSpecFuncStringRepresentation(kind=AggregatorKindEnum.ADJ_LINES_FUNC,
                                                      cmd_inv_as_str=cmd_inv_as_str,
                                                      is_implemented=is_implemented)

    @staticmethod
    def make_aggregator_spec_custom_2_ary_from_cmd_inv_with_transformers(
            flag_option_list_transformer: Optional[TransformerFlagOptionList] = None,
            # pos_config_list_transformer: Optional[TransformerPosConfigList] = None,
            is_implemented: bool = False) -> AggregatorSpec:
        return AggregatorSpecFuncTransformer(kind=AggregatorKindEnum.CUSTOM_2_ARY,
                                             flag_option_list_transformer=flag_option_list_transformer,
                                             # pos_config_list_transformer=pos_config_list_transformer,
                                             is_implemented=is_implemented)

    @staticmethod
    def make_aggregator_spec_custom_2_ary_from_string_representation(
            cmd_inv_as_str: str,
            is_implemented: bool = False) -> AggregatorSpec:
        return AggregatorSpecFuncStringRepresentation(kind=AggregatorKindEnum.CUSTOM_2_ARY,
                                                      cmd_inv_as_str=cmd_inv_as_str,
                                                      is_implemented=is_implemented)

    @staticmethod
    def make_aggregator_spec_custom_n_ary_from_cmd_inv_with_transformers(
            flag_option_list_transformer: Optional[TransformerFlagOptionList] = None,
            # pos_config_list_transformer: Optional[TransformerPosConfigList] = None,
            is_implemented: bool = False) -> AggregatorSpec:
        return AggregatorSpecFuncTransformer(kind=AggregatorKindEnum.CUSTOM_N_ARY,
                                             flag_option_list_transformer=flag_option_list_transformer,
                                             # pos_config_list_transformer=pos_config_list_transformer,
                                             is_implemented=is_implemented)

    @staticmethod
    def make_aggregator_spec_custom_n_ary_from_string_representation(
            cmd_inv_as_str: str,
            is_implemented: bool = False) -> AggregatorSpec:
        return AggregatorSpecFuncStringRepresentation(kind=AggregatorKindEnum.CUSTOM_N_ARY,
                                                      cmd_inv_as_str=cmd_inv_as_str,
                                                      is_implemented=is_implemented)

    @staticmethod
    def return_aggregator_conc_if_none_else_itself(arg: Optional[AggregatorSpec]) -> AggregatorSpec:
        return return_default_if_none_else_itself(arg, AggregatorSpec.make_aggregator_spec_concatenate())



class AggregatorSpecNonFunc(AggregatorSpec):

    def __init__(self,
                 kind: Literal[AggregatorKindEnum.CONCATENATE, AggregatorKindEnum.ADJ_LINES_MERGE, AggregatorKindEnum.ADJ_LINES_SEQ],
                 is_implemented: bool) -> None:
        AggregatorSpec.__init__(self, kind, is_implemented)

    def get_aggregator(self,
                       original_cmd_invocation: CommandInvocationWithIO,
                       inputs_from: List[FileNameOrStdDescriptor],
                       output_to: FileNameOrStdDescriptor
                       ) -> Optional[Aggregator]:
        if not self.is_implemented:
            return None
        if self.kind == AggregatorKindEnum.CONCATENATE:
            # TODO
            return None
        elif self.kind == AggregatorKindEnum.ADJ_LINES_MERGE:
            assert(len(inputs_from) == 1)
            # TODO
            # tr -d '\n' | sed '$a\' seems to do the job -> @KK: Can we join this in one command so no sequence of commands?
            return None
        elif self.kind == AggregatorKindEnum.ADJ_LINES_SEQ:
            assert(len(inputs_from) == 1)
            # TODO
            return None


class AggregatorSpecFuncTransformer(AggregatorSpec):

    def __init__(self,
                 kind: Literal[AggregatorKindEnum.ADJ_LINES_FUNC, AggregatorKindEnum.CUSTOM_2_ARY, AggregatorKindEnum.CUSTOM_N_ARY],
                 flag_option_list_transformer: Optional[TransformerFlagOptionList] = None, # None translates to same as seq
                 # pos_config_list_transformer: Optional[TransformerPosConfigList] = None,
                 is_implemented: bool=False) -> None:
        AggregatorSpec.__init__(self, kind, is_implemented)
        # for now, we keep everything in operand list as it is but substitute streaming input and output
        self.flag_option_list_transformer: TransformerFlagOptionList = \
            TransformerFlagOptionList.return_transformer_same_as_seq_if_none_else_itself(flag_option_list_transformer)

    # note that this changes the parameter original_cmd_invocation
    def get_aggregator(self,
                       original_cmd_invocation: CommandInvocationWithIO,
                       inputs_from: List[FileNameOrStdDescriptor],
                       output_to: FileNameOrStdDescriptor
                       ) -> Optional[Aggregator]:
        if not self.is_implemented:
            return None
        # sanity checks
        if self.kind == AggregatorKindEnum.ADJ_LINES_FUNC:
            assert(len(inputs_from) == 1)
        elif self.kind == AggregatorKindEnum.CUSTOM_2_ARY:
            assert(len(inputs_from) == 2)
        original_cmd_invocation.flag_option_list = self.flag_option_list_transformer.get_flag_option_list_after_transformer_application(original_cmd_invocation.flag_option_list)
        original_cmd_invocation.substitute_inputs_and_outputs_in_cmd_invocation(inputs_from, [output_to])
        return Aggregator.make_aggregator_from_cmd_inv_with_io(original_cmd_invocation, self.kind)


class AggregatorSpecFuncStringRepresentation(AggregatorSpec):

    def __init__(self,
                 kind: Literal[AggregatorKindEnum.ADJ_LINES_FUNC, AggregatorKindEnum.CUSTOM_2_ARY, AggregatorKindEnum.CUSTOM_N_ARY],
                 cmd_inv_as_str: str,
                 is_implemented: bool=False) -> None:
        AggregatorSpec.__init__(self, kind, is_implemented)
        # for now, we keep everything in operand list as it is but substitute streaming input and output
        self.cmd_inv_as_str = cmd_inv_as_str

    def get_aggregator(self,
                       original_cmd_invocation: CommandInvocationWithIO,
                       inputs_from: List[FileNameOrStdDescriptor],
                       output_to: FileNameOrStdDescriptor
                       ) -> Optional[Aggregator]:
        # TODO: compute CommandInvocationWithIO from string representation
        # TODO: in the CA, swap the inputs and outputs
        if not self.is_implemented:
            return None
        if self.kind == AggregatorKindEnum.ADJ_LINES_FUNC:
            assert(len(inputs_from) == 1)
            # TODO
            return None
        elif self.kind == AggregatorKindEnum.CUSTOM_2_ARY:
            assert(len(inputs_from) == 2)
            # TODO
            return None
        elif self.kind == AggregatorKindEnum.CUSTOM_N_ARY:
            # TODO
            return None
