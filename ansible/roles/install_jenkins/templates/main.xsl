<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job@2.38">
    <actions>
        <org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobAction plugin="pipeline-model-definition@1.6.0"/>
        <org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction plugin="pipeline-model-definition@1.6.0">
            <jobProperties/>
            <triggers/>
            <parameters/>
            <options/>
        </org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction>
    </actions>
    <description></description>
    <keepDependencies>false</keepDependencies>
    <properties/>
    <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2.80">
        <script>pipeline {
            agent{
            label &apos;master&apos;
            }
            options {
            timestamps()
            ansiColor(&apos;xterm&apos;)
            }
            stages {
            stage(&apos;clean up workspace&apos;){
            steps{
            dir(&apos;devops&apos;) {
            deleteDir()
            }
            }
            }
            stage(&apos;download files from git&apos;) {
            steps{
            git branch: &apos;{{ branch }}&apos;, url: &apos;https://github.com/karpovichart/devops.git&apos;
            }
            }
            }
            stage(&apos;download files from git&apos;) {
            steps{
            git branch: &apos;{{ branch }}&apos;, url: &apos;https://github.com/karpovichart/devops.git&apos;
            }
            }
            stage(&apos;copy folder to dest&apos;) {
            steps{
            sh &apos;cp -r /home/jenkins/workspace/main/ansible/  /home/tomcat/&apos;
            }
            }
            stage(&apos;running ansible playbooks&apos;) {
            steps {
            ansiblePlaybook(
            becomeUser: &apos;tomcat&apos;,
            colorized: true,
            inventory: &apos;/home/tomcat/hosts.ini&apos;,
            playbook: &apos;/home/tomcat/ansible/pb_install_mysql.yml&apos;)
            }
            steps {
            ansiblePlaybook(
            becomeUser: &apos;tomcat&apos;,
            colorized: true,
            inventory: &apos;/home/tomcat/hosts.ini&apos;,
            {% if side_mode == "double" %}
            playbook: &apos;/home/tomcat/ansible/pb_install_apache.yml &apos;)

            }
            steps {
            ansiblePlaybook(
            becomeUser: &apos;tomcat&apos;,
            colorized: true,
            inventory: &apos;/home/tomcat/hosts.ini&apos;,
            playbook: &apos;/home/tomcat/ansible/pb_install_wp.yml&apos;)
            }
            steps {
            ansiblePlaybook(
            becomeUser: &apos;tomcat&apos;,
            colorized: true,
            inventory: &apos;/home/tomcat/hosts.ini&apos;,
            playbook: &apos;/home/tomcat/ansible/pb_install_nginx.yml&apos;)
            }
            }
            }
            }</script>
        <sandbox>true</sandbox>
    </definition>
    <triggers/>
    <authToken>23432</authToken>
    <disabled>false</disabled>
</flow-definition>
