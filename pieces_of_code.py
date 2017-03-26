# def look_for_keyword_in_libraries(self, tested_keyword):
#     found = False
#     library_keywords = self.get_keywords_from_library()
#     for library_keyword in library_keywords:
#         if tested_keyword and tested_keyword in library_keyword:
#             if self.check_quantity_and_equality(tested_keyword, library_keyword):
#                 found = True
#                 break
#
#     if not found:
#         for library_keyword in library_keywords:
#             m = re.compile(r'^(([A-Za-z0-9]+[ ])+)\ {2,4}.*$').match(tested_keyword)
#             if m:
#                 tested_keyword = m.group(1).rstrip()
#                 if tested_keyword in library_keyword:
#                     if self.check_quantity_and_equality(tested_keyword, library_keyword):
#                         found = True
#                         break
#
#     if not found:
#         for library_keyword in library_keywords:
#             if '$' in tested_keyword:
#                 if self.check_quantity_and_equality(tested_keyword, library_keyword):
#                     found = True
#                     break
#     if self.debug:
#         print 'status', found
#     return found
#
# def get_imports(self, file):
#     keywords_from_scenario = self.get_keywords_usages(file)
#     imports_to_include = []
#     library_files = self.get_library_files()
#     for library_file in library_files:
#         file_to_check = os.path.realpath(library_file)  # .replace('\\', '/')
#         for keyword in keywords_from_scenario:
#             if self.keyword_in_file(file_to_check, self.get_keyword(keyword)):
#                 if file_to_check not in imports_to_include:
#                     imports_to_include.append(file_to_check)
#     return imports_to_include

# def get_keywords_usages(self, file):
#     keywords = []
#     with open(file, 'r') as scenario_file:
#         scenario_lines = scenario_file.readlines()
#         for line in scenario_lines:
#             line_stripped = self.remove_new_line(line)
#             if self.line_contains_bdd_starter(line_stripped):
#                 keywords.append(self.clean_line_from_bdd_starter(line_stripped))
#     return keywords
sss