class Documentor:
    """Convert Javadocs to a web page"""

    def __init__(self, saving_directory, files_path, title, source_url) -> None:
        self._saving_directory = saving_directory
        self._files_path = files_path
        self._title = title
        self._source_url = source_url
        self._header = f'''<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    <title>{self._title}</title>''' + '''
    <style>
        h1 {
            font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
            text-align: center;
        }

        h2 {
            font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        }

        table {
            border-collapse: collapse;
        }

        table, th, td {
            font-family: monospace;
            border: 1px solid black;
            padding: 10px;
        }

        a:hover {
            text-decoration: none;
            color: #ed1c24;
        }

        .panel-title {
            color: #821522;
            font-weight: bolder;
        }

        .panel-collapse {
            color: black;
        }

        .heading {
            font-size: 16px;
            font-weight: bold;
        }

        #type {
            color: #ed7d1c;
        }

        #comm {
            color: #9c9c9c;
            font-style: italic;
        }

        #bool {
            color: cadetblue;
        }
    </style>
</head>'''

    def _get_files(self) -> list:
        """Read the given files

        Returns:
            list: The content of each file
        """
        files = []
        for file in self._files_path:
            with open(file, 'r') as f:
                files.append(f.read())
        return files
    
    def _contain_list(self, lst, params, is_not=False) -> list:
        """Create new list with the elements which have or not the params inside them 

        Args:
            lst (str): The original list
            params (str): The values that need or don't need to be in the elements
            is_not (bool, optional): 
                If true - The new list will contain only the element without the params inside them. Defaults to False.

        Returns:
            list: The new modified list
        """
        new_lst = []

        if not isinstance(params, list):
            params = [params]
        if is_not:
            for param in params:
                new_lst = [l for l in lst if param not in l]
                lst = [l for l in lst if param not in l]
        else:
            for param in params:
                new_lst = [l for l in lst if param in l]
                lst = [l for l in lst if param not in l]
        return new_lst

    def _get_params_dict(self, params_list) -> dict:
        """Create a dictionary with the function parameters

        Args:
            params_list (str): The function parameters list (with the types)

        Returns:
            dict: A dictionary with the parameter name as the key and the parameter type as the value
        """
        params_dict = {}
        i = 0
        while i < len(params_list):
            params_dict[params_list[i + 1]] = params_list[i]
            i += 2
        return params_dict


    def _get_doc_dict(self, lst, p) -> dict:
        dct = {}
        for l in lst:
            l = l.replace(p, '').strip().split(' ')
            dct[l[0]] = ' '.join(l[1:])
        return dct


    def _get_func_info(self, code_block) -> tuple:
        comment = []

        for code in code_block:
            code = code.strip()
            if code[0] == '/':
                code = code[1:].lstrip().split(' ')
                func = code[2:]

                if '(' not in func[0]:
                    return None, None, None, None
                params = []
                for word in func:
                    params.append(word)
                    if ')' in word:
                        break
                
                if len(params) <= 1:
                    params = None
                else:
                    params[0] = params[0].split('(')[1]
                    params[-1] = params[-1].replace(')', '')
                    params = [p.replace(',', '') for p in params]

                    params = self._get_params_dict(params)

                code = code[1:3]
                func_type = code[0].strip()
                if '(' in func_type:
                    return None, None, None, None

                func_name = code[1].split('(')[0]
                break
            else:
                comment.append(code)

        return func_type, func_name, params, comment


    def _filter_comment(self, comment) -> tuple:
        func_description = ' '.join(self._contain_list(comment, ['@param', '@return'], True))
        params_description = self._contain_list(comment, '@param')
        return_description = self._contain_list(comment, '@return') 

        params_description = self._get_doc_dict(params_description, '@param')
        return_description = ''.join(return_description).replace('@return ', '')

        return func_description, params_description, return_description


    def _pannel_body(self, code, tabs) -> str:
        body = tabs + '<ul class="list-group">\n'

        code = code.split('public class')[1].lstrip()
        class_name = code.split(' ')[0]
        
        code = code.replace(class_name, '', 1).lstrip()[1:-2]
        code = code.split('/**')[1:]


        for block in code:
            block = block.strip()
            block = block.replace('\n', ' ')

            if block == '' or block == ' ':
                continue

            block = block.split('*')
            block = [line.strip() for line in block if line]
            type, name, params, comment = self._get_func_info(block)
            if type is None:
                continue
            
            body += tabs + '\t<li class="list-group-item">\n'
            params_str = ""
            if params:
                for key, value in params.items():
                    if params_str:
                        params_str += f', <span id="type">{value}</span> {key}'
                    else:
                        params_str += f'<span id="type">{value}</span> {key.strip()}'

            body += tabs + f'\t\t<code class="heading">{name}({params_str}) -> <span id="type">{type}</span></code>: <br>\n'
            desc, params_desc, return_desc = self._filter_comment(comment)
            body += tabs + f'\t\t<div class="row">\n'
            body += tabs + f'\t\t\t<div class="col-md-8">\n'
            body += tabs + f'\t\t\t\t{desc}<br><br>\n'
            body += tabs + f'\t\t\t</div>\n\t\t</div>\n'
            if params_desc:
                body += tabs + '\t\t<b>Parameters:</b><br>\n'
                for key, value in params_desc.items():
                    body += tabs + f'\t\t<code>{key}</code> - {value}{"." if "." != value[-1] else ""}<br>\n'
            if return_desc:
                body += tabs + f'\t\t<b>Return:</b><br>{return_desc}\n'
            body += tabs + '\t\t<br>\n'
            body += tabs+ '\t</li>\n'

        body += tabs + '</ul>'
        return body


    def _body(self) -> str:
        files = self._get_files()
        body_content = "<body>\n"

        body_content += f'\t<h1><b>{self._title}</b></h1><br>\n'
        body_content += f'\t<p style="text-align: center;"><a href="{self._source_url}" target="_blank">Source Code</a></p>\n'

        for i in range(len(files)):
            code = files[i]
            class_name = code.split('class')[1].strip().split('{')[0].strip()
            body_content += '\t<div class="container">\n\t\t<div class="panel-group">\n\t\t\t<div class="panel panel-default">\n'
            body_content += f'\t\t\t\t<div class="panel-heading"><h4 class="panel-title"><a data-toggle="collapse" href="#collapse{i}">{class_name}</a></h4></div>\n'
            body_content += f'\t\t\t\t<div id="collapse{i}" class="panel-collapse collapse">\n'
            body_content += self._pannel_body(code, '\t\t\t\t\t') + '\n'
            body_content += '\n\t\t\t\t</div>\n'
            body_content += '\t\t\t</div>\n\t\t</div>\n\t</div>'

        body_content += '\n</body>'

        return body_content


    def create(self) -> None:
        all_content = self._header + '\n\n' + self._body()
        with open(f'{self._saving_directory}/{self._title}.html', 'w') as page:
                page.write(all_content)