def kpi_program_table_refresh(self,data:list=[]):
        self.kpi_program_element['table'].setRowCount(0)
        for program_data in data:
            row_number = self.kpi_program_element['table'].rowCount()
            self.kpi_program_element['table'].insertRow(row_number) # Insert row
            self.kpi_program_element['table'].setItem(row_number, 0, QTableWidgetItem(program_data['name'])) # Add name
            self.kpi_program_element['table'].setItem(row_number, 1, QTableWidgetItem(program_data['version'])) #

def kpi_program_get(self,kpi_table_data):
        
        if kpi_table_data == ["running"]  or kpi_table_data == ["error"] or kpi_table_data == [] :
            Log.info(f"KPI program table data have get! {kpi_table_data}")
            # self.program_manager.set_program_data([])
            self.kpi_program_table_refresh([])

            return
        else:
            Log.info(f"kpi kpi_program_get signal -> {kpi_table_data[0:1]} {self}")
                # Log.info(f"KPI program table data have get! finished")
            data_invald:list[dict]=[]
            self.program_manager.set_program_data(kpi_table_data)
            if self.kpi_program_element['search_edit'].text()!='':
                for program_data in self.program_manager.get_program_data():
                    for key,value in program_data.items():
                        if  self.kpi_program_element['search_edit'].text() in value:
                            data_invald.append(program_data)
                            break
                self.kpi_program_table_refresh(data=data_invald)
            else:
                self.kpi_program_table_refresh(data= self.program_manager.get_program_data())
            return


