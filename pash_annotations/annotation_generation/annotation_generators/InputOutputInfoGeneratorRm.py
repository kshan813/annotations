from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorRm(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        self.all_operands_are_other_outputs()