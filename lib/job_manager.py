import jenkins
from typing import Any, List
from lib.xml_handler import XmlHandler, keys_to_camel_case


class BaseJob:
    """
    Render base job config with different types of parameters
    """

    def __init__(self, description: str, base_xml: str = jenkins.EMPTY_CONFIG_XML):
        self._xml_handler = XmlHandler(base_xml)
        self._project = self._xml_handler.data.project
        self._project.description = description

    def _add_generic_parameter(self, parameter_type: str, parameter_dict: dict) -> None:
        parameter_dict = keys_to_camel_case(parameter_dict)
        hudson_model_parameter_type = f"hudson.model.{parameter_type}"
        if self._project.get('properties') is None:
            self._project.properties = {"hudson.model.ParametersDefinitionProperty":
                                            {'parameterDefinitions':
                                                 {}
                                             }
                                        }

        parameter_definitions_context = self._project.properties[
            "hudson.model.ParametersDefinitionProperty"].parameterDefinitions
        if parameter_definitions_context.get(hudson_model_parameter_type) is None:
            parameter_definitions_context[hudson_model_parameter_type] = [parameter_dict]
        else:
            hudson_model_parameter_type_list = \
            self._project.properties['hudson.model.ParametersDefinitionProperty'].parameterDefinitions[
                hudson_model_parameter_type]
            hudson_model_parameter_type_list.append(parameter_dict)

    def add_job_choices_parameter(
            self, name: str, description: str, choices: List[str], parameter_type="ChoiceParameterDefinition"
    ) -> None:
        """
        Add choices (options) parameter to the job
        @param name: parameter name
        @param description: description
        @param choices: list of choices (options)
        @param parameter_type: Jenkins specific type of parameter
        @return: None
        """
        parameter_dict = {"name": name, "description": description}
        choices_entry = {"@class": "java.util.Arrays$ArrayList", "a": {"@class": "string-array", "string": choices}}
        parameter_dict["choices"] = choices_entry

        self._add_generic_parameter(parameter_type, parameter_dict)

    def add_job_parameter(
            self,
            name: str,
            description: str,
            default_value: Any,
            trim: bool = False,
            parameter_type: str = "StringParameterDefinition",
    ):
        """
        Add string parameter to the job
        @param name: name of parameter
        @param description: description
        @param default_value: default value
        @param trim: trim
        @param parameter_type: Jenkins specific type of parameter
        @return: None
        """

        parameter_dict = dict(name=name, description=description, default_value=default_value, trim=trim)
        self._add_generic_parameter(parameter_type, parameter_dict)

    def unparse(self) -> str:
        return self._xml_handler.unparse()


class FreestyleJob(BaseJob):
    def _add_builder(self, script: str, task_type="BatchFile", configured_local_rules=None) -> None:
        """
        Add build step to Jenkins job
        @param script: script content
        @param task_type: task type
        @param configured_local_rules: configured local rules
        @return: None
        """
        hudson_task_type = f"hudson.tasks.{task_type}"
        hudson_task_entry = {"command": script, "configuredLocalRules": configured_local_rules}
        if self._project.builders is None:
            self._project.builders = {hudson_task_type: [hudson_task_entry]}
        else:
            self._project.builders[hudson_task_type].append(hudson_task_entry)

    def add_builder_shell_script(self, script, configured_local_rules=None) -> None:
        self._add_builder(script=script, task_type="Shell", configured_local_rules=configured_local_rules)

    def add_artifact_archiver(
            self,
            artifacts: str,
            allow_empty_archive: bool = False,
            only_if_successful: bool = False,
            fingerprint: bool = False,
            default_excludes: bool = True,
            case_sensitive: bool = True,
            follow_symlinks: bool = False,
    ) -> None:
        """
        Add artifact collector to Jenkins job. !! ArtifactArchiver plugin must be installed !!
        @param artifacts: string of artifacts expression
        @param allow_empty_archive: allow empty archive
        @param only_if_successful: only if successful
        @param fingerprint: fingerprint
        @param default_excludes: default excludes
        @param case_sensitive: case sensitive
        @param follow_symlinks: follow symlinks
        @return: None
        """
        hudson_task_type = "hudson.tasks.ArtifactArchiver"

        artifacts_elem = keys_to_camel_case(
            dict(
                artifacts=artifacts,
                allow_empty_archive=allow_empty_archive,
                only_if_successful=only_if_successful,
                fingerprint=fingerprint,
                default_excludes=default_excludes,
                case_sensitive=case_sensitive,
                follow_symlinks=follow_symlinks
            )
        )

        if self._project.publishers is None:
            self._project.publishers = {hudson_task_type: artifacts_elem}
        else:
            self._project.publishers[hudson_task_type] = artifacts_elem
