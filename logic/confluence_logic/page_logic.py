from calls.confluence_api_calls.conf_api_pages import ConfluencePageCalls
from bs4 import BeautifulSoup


class Pages:
    def __init__(self,  is_staging=False):
        self.conf_pages = ConfluencePageCalls(is_staging=True) if is_staging else ConfluencePageCalls()

    def create_page(self, space_key, title, content, ancestors):
        page_type = 'page'
        result = self.conf_pages.create_content(page_type, space_key, title, content, ancestors)

        return result

    def generate_table_header(self, headers):
        # Create the table header based on the list of column names
        table_header = "<table>\n  <thead>\n    <tr>\n"
        for header in headers:
            table_header += f"      <th>{header}</th>\n"
        table_header += "    </tr>\n  </thead>\n  <tbody>\n"
        return table_header

    def generate_table_content(self, projects, headers):
        # Generate the table header
        table_content = self.generate_table_header(headers)

        # Loop through the project data and create table rows
        for project in projects:
            table_content += "    <tr>\n"
            for header in headers:
                table_content += f"      <td>{project.get(header.lower().replace(' ', '_'), '')}</td>\n"
            table_content += "    </tr>\n"

        # Close the table
        table_content += "  </tbody>\n</table>\n"

        return table_content

    def parse_table(self, page_content):
        soup = BeautifulSoup(page_content, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')
        table_data = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if cols:
                table_data.append(cols)
        return table_data, soup, table

    def update_table_row(self, table, project_key_to_find, new_approver):
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if cols and len(cols) > 1:
                project_key = cols[1].text.strip()
                if project_key == project_key_to_find:
                    approver = cols[2].text.strip()
                    if approver != new_approver:
                        cols[2].string.replace_with(new_approver)
                        return True
        return False

    def update_approver_in_page(self, page_id, project_key_to_find, new_approver):
        # Get the page content
        page_data = self.conf_pages.get_page(page_id)

        if not page_data:
            return

        # Extract page content and version
        page_content = page_data['body']['storage']['value']
        version = page_data['version']['number']
        title = page_data['title']
        page_type = 'page'

        # Parse the table
        table, soup = self.parse_table(page_content)

        # Update the table row if necessary
        if table:
            updated = self.update_table_row(table, project_key_to_find, new_approver)
            if updated:
                updated_page_content = str(soup)
                self.conf_pages.update_content(page_id, page_type, title, updated_page_content, version)
            else:
                print("No update needed; approver already correct.")
        else:
            print("Table not found in the page content.")

    def clear_page_content(self, page_id):
        page_data = self.conf_pages.get_page(page_id)
        if not page_data:
            return False

        current_version = page_data['version']['number']
        page_title = page_data['title']
        page_type = page_data['type']

        if self.conf_pages.update_content(page_id, page_type, page_title, "", current_version):
            print(f"Content of page '{page_id}' cleared successfully!")
            return True
        else:
            print(f"Failed to clear content of page '{page_id}'.")
            return False

    def get_page_version(self, page_id):
        page_data = self.conf_pages.get_page(page_id)
        return page_data['version']['number']

    def get_page_type(self, page_id):
        page_type = self.conf_pages.get_page(page_id)
        return page_type['type']

    def update_page(self, page_id, page_title, content):
        page_version = self.get_page_version(page_id)
        page_type = self.get_page_type(page_id)

        response = self.conf_pages.update_content(page_id, page_type, page_title, content, page_version)
        return response

    def delete_page(self, page_id):
        response = self.conf_pages.delete_page(page_id)
        return response

    def add_user_edit_to_pages_restriction(self, page_ids, account_id):
        for page_id in page_ids:
            # Call the function to add the user to each page restriction
            self_add = self.conf_pages.add_self_to_page_restriction(page_id)

            if self_add.status_code == 200:
                print(f"Successfully added you to {page_id} for edit access.")
            elif self_add.status_code == 404:
                print(f"Page {page_id} not found.")
                return self_add.status_code
            else:
                print(f"Failed to add you to page {page_id}: {self_add.status_code}, {self_add.text}")
                return self_add.status_code

            response = self.conf_pages.add_restrictions_to_page(page_id, "update", account_id)

            if response.status_code == 200:
                print(f"Successfully added user {account_id} to page {page_id} for edit access.")
            elif response.status_code == 404:
                print(f"Page {page_id} not found.")
            else:
                print(f"Failed to add user {account_id} to page {page_id}: {response.status_code}, {response.text}")

    def add_user_read_to_pages_restriction(self, page_ids, account_id):
        for page_id in page_ids:

            self_add = self.conf_pages.add_self_to_page_restriction(page_id)

            if self_add.status_code == 200:
                print(f"Successfully added you to {page_id} for edit access.")
            elif self_add.status_code == 404:
                print(f"Page {page_id} not found.")
                return self_add.status_code
            else:
                print(f"Failed to add you to page {page_id}: {self_add.status_code}, {self_add.text}")
                return self_add.status_code

            # Call the function to add the user to each page restriction
            response = self.conf_pages.add_user_to_page_restriction(page_id, "read", account_id)

            if response.status_code == 200:
                print(f"Successfully added user {account_id} to page {page_id} for read access.")
            elif response.status_code == 404:
                print(f"Page {page_id} not found.")

            else:
                print(f"Failed to add user {account_id} to page {page_id}: {response.status_code}, {response.text}")


