from glob import glob
import os
import re
import tempfile


class TestGenerator(object):
    files = glob('./*.txt')
    bdd_starters = ['When', 'And', 'Then', 'Given']

    def __init__(self):
        self.debug = False
        self.scenario_name = ''
        self.test_steps = []
        self.common_ancestors = []
        self.keywords_files  = self.get_library_files('.\\Keywords')

        # exit(0)

    def get_library_files(self, catalog):
        lib_files = []
        for root, dir, files in os.walk(catalog):
            for file in files:
                filepath = os.path.join(root, file)
                # parent_dcit = self.check_imports(catalog, filepath)
                # print 'parent_dcit', parent_dcit
                # self.common_ancestors.append(parent_dcit)
                lib_files.append(filepath)
        return lib_files

    # def check_imports(self, catalog, filepath):
    #     parent_dict = {}
    #     parent, child, child_multiple_parents = TestGenerator.get_file_parent(catalog, filepath)
    #     if parent and child:
    #         if parent not in parent_dict:
    #             parent_dict[parent] = child
    #         else:
    #             parent_dict[parent] += ','+child
    #
    #     for library, parents_of_library in child_multiple_parents.iteritems():
    #         if len(parents_of_library.split(',')) > 1:
    #             print 'Caution, multiple imports of the same resource!' \
    #                   '\r\nResource files importing resource "{}": \r\n{}'\
    #                 .format(library,''.join(['{}\r\n'.format(parent) for parent in parents_of_library.split(',')]))
    #             return False
    #
    #     return parent_dict

    def get_common_ancestor(self, imports_to_verify):
        common_ancestor = ''
        if len(imports_to_verify) >=2:
            import_one = imports_to_verify[0]
            for import_second in imports_to_verify[1:]:
                import_two = import_second
                print 'import one', import_one
                print 'import_two', import_two
                print 'self.common_ancestors', self.common_ancestors
                for common_ancestor_element in self.common_ancestors:
                    print 'common_ancestor_element', common_ancestor_element
                    for ancestor, child_libraries in common_ancestor_element.iteritems():
                        print 'ancestor {} child_libraries {}'.format(ancestor, child_libraries)
                        print 'ancestor', ancestor
                        print 'child_libraries', child_libraries
                        if '{},{}'.format(import_one, import_two) == child_libraries \
                            or '{},{}'.format(import_two, import_one) == child_libraries:
                            common_ancestor = ancestor
        return common_ancestor

    # @staticmethod
    # def get_file_parent(catalog, library_file):
    #     parent, child = None, None
    #     child_has_parents = {}
    #     for root, dir, files in os.walk(catalog):
    #         for file in files:
    #             file_to_be_parent = os.path.join(root, file)
    #             if file_to_be_parent != library_file:
    #                 with open(file_to_be_parent, 'r') as parent_content:
    #                     content_to_be_checked = parent_content.readlines()
    #                     for line_of_content in [content_line.rstrip().rstrip('\r\n') for content_line in content_to_be_checked]:
    #                         if 'Resource' in line_of_content:
    #                             if library_file.replace(catalog, '').replace('\\', '/') in line_of_content:
    #                                 parent = file_to_be_parent
    #                                 child = library_file
    #                                 if child not in child_has_parents:
    #                                     child_has_parents[child] = parent
    #                                 else:
    #                                     child_has_parents[child] += parent
    #
    #     return parent, child, child_has_parents

    @staticmethod
    def get_char_number(string, character):
        return string.count(character)

    @staticmethod
    def remove_new_line(line):
        return line.strip(os.linesep)

    @staticmethod
    def line_contains_bdd_starter(line):
        string_found = False
        for string in TestGenerator.bdd_starters:
            if string in line:
                string_found = True
                break
        return string_found

    @staticmethod
    def make_list(element):
        return [element] if not isinstance(element,list) else element

    @staticmethod
    def clean_line_from_bdd_starter(line):
        line_to_check = line
        for bdd_starter in TestGenerator.bdd_starters:
            if bdd_starter in line_to_check:
                line_to_check = line_to_check.replace(bdd_starter + ' ', '')
        clean_keyword = line_to_check.strip()
        return clean_keyword

    @staticmethod
    def get_name_of_scenario(filename):
        characters_to_remove = '`~!@#$%^&*()_+={}[]\\|?,<.>/?'
        rules = {' ': '_'}
        name_of_scenario = os.path.splitext(os.path.basename(filename))[0]
        for character in characters_to_remove:
            if character in name_of_scenario:
                name_of_scenario = name_of_scenario.replace(character, '')
        return name_of_scenario

    @staticmethod
    def get_keyword(scenario_step):
        step_to_verify = TestGenerator.clean_line_from_bdd_starter(scenario_step)
        m = re.compile(r'^(([A-Za-z0-9]+[ ])+)\ {1,4}.*$').match(step_to_verify)
        return m.group(1).rstrip() if m else step_to_verify

    def verify_keyword_arguments(self, scenario_step):
        step_to_verify = TestGenerator.clean_line_from_bdd_starter(scenario_step)
        argument = []
        if TestGenerator.get_char_number(scenario_step, '$') <= 1:
            m = re.compile(r'^.*( {2,4}(\$\{[A-Za-z0-9_\- ]+\}|[A-Za-z0-9]+))$').match(step_to_verify)
            if m:
                argument.append(m.group(1).strip())
                if len(argument) == 0 and TestGenerator.get_char_number(scenario_step, '$') == 1:
                    return False
            else:
                m = re.compile(r'^.*( (\$\{[A-Za-z0-9\- ]+\}) ).*$').match(step_to_verify)
                if m:
                    argument.append(m.group(1).strip())
                else:
                    m = re.compile(r'^.*( {2,4}([A-Za-z0-9\`\~\,\.\,<>\?/:;\'\"\- '
                                   r'\$\}\{\[\]\!\@\#\$\%\^\&\*\(\)_\+\|\\=]+))$').match(step_to_verify)
                    if m:
                        return False
            if len(argument) == 0 and TestGenerator.get_char_number(scenario_step, '$') == 0:
                return True
        else:
            for scenario_step_part in scenario_step.split():
                m = re.compile(r'^\$\{[A-Za-z0-9\-_ ]+\}$').match(scenario_step_part)
                if m:
                    if m.group(0) not in argument:
                        argument.append(m.group(0).strip())
                if len(argument) == TestGenerator.get_char_number(scenario_step, '$'):
                    return True
        return argument

    def verify_keyword(self, keywords_to_check):
        keyword_in_libraries = False
        for test_keyword in TestGenerator.make_list(keywords_to_check):
            keyword_in_libraries = self.search_keyword_in_libraries(TestGenerator.get_keyword(test_keyword))
        return keyword_in_libraries

    def search_keyword_in_libraries(self, tested_keyword):
        found = False
        library_keywords = self.get_keywords_from_library()
        for library_keyword in library_keywords:
            if tested_keyword and tested_keyword in library_keyword:
                if self.check_quantity_and_equality(tested_keyword, library_keyword):
                    found = True
                    break
            else:
                m = re.compile(r'^(([A-Za-z0-9]+[ ])+)\ {2,4}.*$').match(tested_keyword)
                if m:
                    tested_keyword = m.group(1).rstrip()
                    if self.check_quantity_and_equality(tested_keyword, library_keyword):
                        found = True
                        break
                else:
                    if '$' in tested_keyword:
                        if self.check_quantity_and_equality(tested_keyword, library_keyword):
                            found = True
                            break
        return found

    def check_quantity_and_equality(self, tested_keyword, library_keyword):
        equal = False
        tested_keyword_words = tested_keyword.split()
        library_keyword_words = library_keyword.split()
        if len(tested_keyword_words) == len(library_keyword_words) \
                and TestGenerator.get_char_number(tested_keyword, ' ') == TestGenerator.get_char_number(library_keyword, ' '):
            for tested_keyword_word, library_keyword_word in zip(tested_keyword_words, library_keyword_words):
                if '$' in tested_keyword_word and '$' not in library_keyword_word:
                    equal = False
                    break
                if '$' not in tested_keyword_word and '$' in library_keyword_word:
                    equal = False
                    break
                if '$' not in tested_keyword_word and '$' not in library_keyword_word:
                    if len(tested_keyword_word) == len(library_keyword_word):
                        if tested_keyword_word == library_keyword_word:
                            equal = True
                        else:
                            equal = False
                            break
                    else:
                        equal = False
                        break
                else:
                    if tested_keyword_word.startswith('${') and tested_keyword_word.endswith('}'):
                        equal = True
                    else:
                        equal = False
                        break
        return equal

    def get_imports(self):
        keywords_from_scenario = [TestGenerator.clean_line_from_bdd_starter(step) for step in self.test_steps]
        imports_to_include = []
        for library_file in self.keywords_files:
            for keyword in keywords_from_scenario:
                if self.keyword_in_file(library_file, TestGenerator.get_keyword(keyword)):
                    if library_file not in imports_to_include:
                        imports_to_include.append(library_file)

        # imports_to_in = [import_line.replace('\\', '/') for import_line in imports_to_include]
        # print 'imports_to_include', imports_to_in
        # anc = self.get_common_ancestor(imports_to_in)
        # print 'anc', anc
        # if anc:
        #     return anc

        return imports_to_include

    def get_test_steps(self, file):
        test_steps = []
        with open(file, 'r') as scenario_file:
            scenario_lines = scenario_file.readlines()
            for line in scenario_lines:
                line_stripped = TestGenerator.remove_new_line(line)
                if TestGenerator.line_contains_bdd_starter(line_stripped):
                    test_steps.append(line_stripped)
        return test_steps

    def get_keywords_from_library(self):
        keywords = []
        for library_file in self.keywords_files:
            with open(library_file, 'r') as library_file_to_read:
                lines = library_file_to_read.readlines()
                for line in lines:
                    line_stripped = TestGenerator.remove_new_line(line)
                    m = re.compile('^[A-Za-z]{1,}[\$_-\{\} ].*$').match(line_stripped)
                    not_included = ['Documentation']
                    if m:
                        for not_inc in not_included:
                            if not_inc not in m.group(0):
                                keywords.append(line_stripped)
        return keywords

    def keyword_in_file(self, library_or_resource_file, keyword_to_find):
        found = False
        with open(library_or_resource_file, 'r') as file_to_be_checked:
            content = file_to_be_checked.readlines()
            for line in content:
                line = line.strip(os.linesep)
                if keyword_to_find == line:
                    found = True
                    break
        return found

    def get_tags_list(self):
        tags = ['DEMO123', 'Tag1', 'tag2', 'tag3']
        tags_list = os.linesep.join([tags[0]+' '+' '.join(tags[1:])])
        return tags_list

    def do_stuff_in_jira(self, comment_text):
        """
        Method do_stuff_in_jira - first it should got better name, then it will be reporting status of scenario to jira.
        :param comment_text: it contains lines with information about current errors and problems
                             in each line of scenario.
        :return: for now it does not returns anything
        """
        print 'Adding comment to jira ticket, changing status to "Ready for automation", ' \
              'assigning ticket to reporter, ... etc'
        print 'Errors: \r\n',comment_text

    def check_scenario_lines(self, file):
        """
        Check scenario lines - method used to verify if lines in scenario are properly filled with keywords, arguments.
        :param file: name of file to be verified
        :return:
        """
        lines_with_errors = {}
        line_number = 0
        with open(file, 'r') as scenario_file:
            self.scenario_name = TestGenerator.get_name_of_scenario(file)
            scenario_lines = scenario_file.readlines()
            self.test_steps = self.get_test_steps(file)
            if not scenario_lines:
                return False
            else:
                for line in scenario_lines:
                    line_number += 1
                    line = TestGenerator.remove_new_line(line)
                    if self.debug:
                        print 'scenario line "{}"'.format(line)
                    is_blank_line = bool(line == '')
                    if is_blank_line:
                        lines_with_errors[line_number] = {'content': line, 'empty': is_blank_line,
                                                          'missing_bdd': False, 'missing_keyword': False,
                                                          'argument_issue': False}
                    if not TestGenerator.line_contains_bdd_starter(line):
                        lines_with_errors[line_number] = {'content': line, 'empty': is_blank_line,
                                                          'missing_bdd': True, 'missing_keyword': False,
                                                          'argument_issue': False}
                    else:
                        if not self.verify_keyword(line):
                            lines_with_errors[line_number] = {'content': line, 'empty': is_blank_line,
                                                              'missing_bdd': False, 'missing_keyword': True,
                                                              'argument_issue': False}
                        else:
                            if not self.verify_keyword_arguments(line):
                                lines_with_errors[line_number] = {'content': line, 'empty': is_blank_line,
                                                                  'missing_bdd': False, 'missing_keyword': False,
                                                                  'argument_issue': True}
                            else:
                                # final check of scenario - use pybot --dryrun :)
                                pass

                if lines_with_errors:
                    comment_text = 'Scenario "{}" needs work.\r\n'.format(self.scenario_name)
                    for line_no in sorted(lines_with_errors):
                        if lines_with_errors[line_no]['empty']:
                            comment_text += 'Line no {}: is empty - please remove it.\r\n'.format(line_no)
                        elif lines_with_errors[line_no]['missing_bdd']:
                            comment_text += 'Line no {}: "{}" has not BDD starting part - please verify it.\r\n'\
                                .format(line_no, lines_with_errors[line_no]['content'])
                        elif lines_with_errors[line_no]['missing_keyword']:
                            comment_text += 'Line no {}: "{}" contains not defined keyword(s) or just needs fix(es).\r\n'\
                                .format(line_no, lines_with_errors[line_no]['content'])
                        elif lines_with_errors[line_no]['argument_issue']:
                            comment_text += 'Line no {}: "{}" contains improper argument(s).\r\n' \
                                .format(line_no, lines_with_errors[line_no]['content'])
                    self.do_stuff_in_jira(comment_text)
                    exit(0)
                else:
                    return True

    def prepare_test_case(self, file):
        """
        Prepare test case - method used to start whole process of generating robot test file from scenario in file.
        It returns nothing, only creates robot test files according to list of files.
        :param file: path to file with scenario
        """
        for file in TestGenerator.files:
            if self.check_scenario_lines(file):
                documentation = 'Some weird stuff to include in one line :) - so far, only one line is supported.'
                imports = self.get_imports()
                imports_to_inc = os.linesep.join(['Resource${tab}'+import_line for import_line in imports])
                test_steps = os.linesep.join(['${tab}' + test_step for test_step in self.test_steps])
                test_body_schema = "*** Settings ***${line_sep}" \
                                   "${imports}${line_sep}" \
                                   "Documentation${tab}${documentation}${line_sep}${line_sep}" \
                                   "*** Test Cases ***${line_sep}" \
                                   "${test-title}${line_sep}" \
                                   "${tab}[Tags]${tab}${tags}${line_sep}" \
                                   "${steps}"
                test_body_schema = test_body_schema.replace('${imports}', imports_to_inc)
                test_body_schema = test_body_schema.replace('${documentation}', documentation)
                test_body_schema = test_body_schema.replace('${test-title}', self.scenario_name)
                test_body_schema = test_body_schema.replace('${tags}', self.get_tags_list())
                test_body_schema = test_body_schema.replace('${steps}', test_steps)
                test_body_schema = test_body_schema.replace('${tab}', '    ')
                test_body_schema = test_body_schema.replace('${line_sep}', os.linesep)
                test_body_schema = test_body_schema.replace(os.linesep, '\n')
                print '\r\n******************************START*************************************'
                print test_body_schema
                print '\r\n*******************************END**************************************'
                # tmp_dir = tempfile.gettempdir()
                # tmp_dir = 'C:\\Users\\Kostek\\PycharmProjects\\GeneratingRobotFiles'
                # tmp_test_path = tmp_dir + os.sep + 'tmp_test_{}.robot'.format(self.scenario_name)
                # with open(tmp_test_path, 'w') as temp_test:
                #     temp_test.write(test_body_schema.strip(os.linesep))

if __name__ == "__main__":
    tg = TestGenerator()
    tg.prepare_test_case(TestGenerator.files)
