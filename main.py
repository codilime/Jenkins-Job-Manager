from lib import jenkins_api, job_manager

server = jenkins_api.get_jenkins_server()

# Get 'dummy job' config.xml
xml_data = server.get_job_config('dummy job')

# Create freestyle job
freestyle_job = job_manager.FreestyleJob(description='new dummy job')

# Add string parameters to the job
parameter1 = 'Param1'
parameter2 = 'Param2'
freestyle_job.add_job_parameter(parameter1, description='first parameter', default_value='val1')
freestyle_job.add_job_parameter(parameter2, description='second parameter', default_value='val2')

# Add choices parameter
platform_parameter = 'platform'
freestyle_job.add_job_choices_parameter(platform_parameter, choices=['linux', 'windows'], description='choose platform')

# Add artifact archiver
freestyle_job.add_artifact_archiver('*.log')

# Define builder shell script
freestyle_job.add_builder_shell_script(
    f'''
    echo Selected platform: ${platform_parameter}
    echo Executing job with parameters {parameter1}=${parameter1}, {parameter2}=${parameter2}
    pip list | tee text.log
    '''
)


server.reconfig_job('dummy job', config_xml=freestyle_job.unparse())