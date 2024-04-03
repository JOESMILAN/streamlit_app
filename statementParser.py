from pdfminer.high_level import extract_pages
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

class BankStatement():

    def __init__(self, file):
        self.file = file

    def read_statement(self):
        """
        Function to parse each line and return a dataframe containing the coords of the line and the text within.
        """
        self.raw_df = pd.DataFrame()

        try:
            pages = extract_pages(self.file)

            for page_layout in pages:
                data = []
                for ind, element in enumerate(page_layout):
                    if (element.__class__.__name__ == "LTTextBoxHorizontal") and (ind>=26):
                        for each_element in element: data.append((each_element.x0, each_element.y0, each_element.x1, each_element.y1, each_element.get_text()))

                tmp = pd.DataFrame(data, columns=['x0', 'y0', 'x1', 'y1', 'text'])
                tmp = tmp.sort_values(by=['y0', 'x0'], ascending = [False, True])[3:]
                self.raw_df = pd.concat([self.raw_df, tmp])
        
        except:
            raise('Could not work with the pdf file. Please recheck the file format and path')

    def get_indices_of_column_starts(self):
        '''
        Helper function to group multi line records into one.
        The start coord of the line is used for grouping.
        '''
        # find the start of the first column
        start = self.raw_df['x0'].min()

        # reset the index of df
        self.raw_df = self.raw_df.reset_index(drop=True)

        # get indices of column starts
        indices = self.raw_df[self.raw_df['x0']==start].index.values.tolist()

        return indices

    def partition_df(self):
        '''
        Partitions the dataframe into smaller chunks, where each chunk constitutes 
        to a single record which is present as multiple lines in the document
        '''
        self.indices = self.get_indices_of_column_starts()

        for ind in range(1, len(self.indices)):
            yield self.raw_df.iloc[self.indices[ind-1]: self.indices[ind]]

    def structure_the_data(self):
        '''
        Function to merge/join the multi lines into one.
        Checks the overlap between start and end columns to combine rows
        '''

        data = []
        self.df = pd.DataFrame()
        for part in self.partition_df():
            part = part.reset_index(drop=True)
            if len(part) >= 2:  # Check if DataFrame has at least two rows
                part.loc[0, 'text'] = ' '.join(part['text'][(part['x0']>=part['x0'].iloc[0]) & (part['x0']<=part['x1'].iloc[0])].values.tolist()).replace('\n', '')
                part.loc[1, 'text'] = ' '.join(part['text'][(part['x0']>=part['x0'].iloc[1]) & (part['x0']<=part['x1'].iloc[1])].values.tolist()).replace('\n', '')
                cols = part['text'].values.tolist()[:6]  # Get the first 6 values
                data.append(tuple(map(lambda x: x.replace('\n', ''), cols)))

        self.df = pd.DataFrame(data, columns=['Txn Date', 'Value Date', 'Description', 'Ref No./Cheque No.', 'Debit', 'Credit'])

    def correct_df_columns(self):
        '''
        Helper function that corrects any issues in the DataFrame columns
        '''
        self.df['Debit'] = self.df['Debit'].apply(lambda val: '-' + val.replace('(Dr)', '') if '(Dr)' in val else  val.replace('(Cr)', ''))
        self.df['Credit'] = self.df['Credit'].apply(lambda val: '-' + val.replace('(Dr)', '') if '(Dr)' in val else val.replace('(Cr)', ''))

    def parse_statement_as_df(self):
        self.read_statement()
        self.structure_the_data()
        self.correct_df_columns()
        return self.df
