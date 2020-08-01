from flask_table import (Col,LinkCol, Table,
	create_table)

# class CalendarTable(Table):
# 	""" A table for showing the results of the search """
# 	border = True
# 	allow_sort = False
# 	no_items = "No Results"
# 	html_attrs = {"style":'font-size:18px',} # gets assigned to table header
# 	table_id = 'calendar_results_table' # override this when you make an instance if you dont want vertical layout by default
# 	# column_html_attrs = {'style':'text-align: center; min-width:10px', 'bgcolor':"#FF0000"} # gets assigned to both th and td
# 	# column_html_attrs = [] # javascript tableswapper does not preserve these.
# 	column_html_attrs = {'style':'word-wrap: break-word; max-width:200px;'}

# 	classes = ["table-striped"] # gets assigned to table classes. 
# 	# Striped is alternating bright and dark rows for visual ease.
	
# 	username = Col('username',column_html_attrs=column_html_attrs)
# 	request_name = Col('request name',column_html_attrs=column_html_attrs)
# 	description = Col('description',column_html_attrs=column_html_attrs)
# 	species = Col('species',column_html_attrs=column_html_attrs)
# 	number_of_samples = Col('number of samples',column_html_attrs=column_html_attrs)

def create_dynamic_calendar_table(contents,table_id='',ignore_columns=[],name='Dynamic Calendar Table', **sort_kwargs):
	""" Table showing all samples of a given request, used in the 
	request_overview() route """

	options = dict(
		border = True,
		allow_sort = False,
		no_items = "No Results",
		html_attrs = {"style":'font-size:18px;'},
		table_id = table_id,
		classes = ["table-striped","mb-4"]
		) 
	column_html_attrs = {'style':'word-wrap: break-word; max-width:200px;'}
	table_class = create_table(name,options=options)
	""" Now loop through all columns and add them to the table,
	only adding the imaging modes if they are used in at least one
	sample """
	""" Add the columns that you want to go first here.
	It is OK if they get duplicated in the loop below -- they
	will not be added twice """
	for i in range(2):
		table_class.add_column(f"day_{i}",Col('day {i}'))
	# table_class.add_column('sample_name',Col('sample name',column_html_attrs=column_html_attrs))    
	# table_class.add_column('request_name',Col('request name',column_html_attrs=column_html_attrs))
	# table_class.add_column('username',Col('username',column_html_attrs=column_html_attrs))
	# archival_tooltip_text = ('An archival request is a request '
	# 	'that was not submitted through this web portal, '
	# 	'but was manually entered after the experiment '
	# 	 'was already done. As a result, information may be incomplete '
	# 	 'and not all data products or visualizations may be available.')
	# archival_html_attrs = {'class':'infolink','title':archival_tooltip_text}
	# table_class.add_column('is_archival',BooltoStringCol('archival?',column_html_attrs=column_html_attrs,
	# 	th_html_attrs=archival_html_attrs))
	# table_class.add_column('clearing_protocol',
	# 	Col('clearing protocol',column_html_attrs=column_html_attrs))
	
	# table_class.add_column('clearer',
	# 	NotAssignedCol('clearer',column_html_attrs=column_html_attrs))
	# table_class.add_column('clearing_progress',
	# 	Col('clearing progress',column_html_attrs=column_html_attrs))

	# clearing_url_kwargs = {'username':'username','request_name':'request_name',
	# 	'clearing_protocol':'clearing_protocol',
	# 	'antibody1':'antibody1','antibody2':'antibody2','clearing_batch_number':'clearing_batch_number'}
	# anchor_attrs = {}
	# table_class.add_column('view_clearing_link',
	# 	 ClearingTableLinkCol('Clearing log', 
	# 	'clearing.clearing_table',url_kwargs=clearing_url_kwargs,
	#    anchor_attrs=anchor_attrs,allow_sort=False,column_html_attrs=column_html_attrs))
	
	# imaging_request_subtable_options = {
	# 'table_id':f'imaging_requests',
	# 'border':True,
	# }
	# imaging_requests_subtable_class = create_table('imaging_request_subtable',
	# 	options=imaging_request_subtable_options)
	# imaging_request_url_kwargs = {'username':'username',
	# 	'request_name':'request_name','sample_name':'sample_name',
	# 	'imaging_request_number':'imaging_request_number'}
	# imaging_requests_subtable_class.add_column('imaging_request_number',
	# 	ImagingRequestLinkCol('imaging request number','imaging.imaging_table',
	# 		url_kwargs=imaging_request_url_kwargs,column_html_attrs=column_html_attrs))
	# imaging_requests_subtable_class.add_column('imager',
	# 	NotAssignedCol('imager',column_html_attrs=column_html_attrs))
	# imaging_requests_subtable_class.add_column('imaging_progress',
	# 	Col('imaging progress',column_html_attrs=column_html_attrs))
	# imaging_url_kwargs = {'username':'username','request_name':'request_name','sample_name':'sample_name'}
	# new_imaging_request_tooltip_text = ('Not available for archival requests. '
	# 	'Please only request additional imaging for this sample '
	# 	'if your original request did not cover the sufficient imaging. '
	# 	 'To see what imaging you have already requested, '
	# 	 'click on the existing imaging request number(s) for this sample. '
	# 	 'If this field shows "N/A" it is because no additional imaging is possible for this sample.')
	# new_imaging_request_html_attrs = {'class':'infolink','title':new_imaging_request_tooltip_text}

	# table_class.add_column('new imaging request',
	# 	NewImagingRequestLinkCol('request additional imaging','imaging.new_imaging_request',
	# 		url_kwargs=imaging_url_kwargs,th_html_attrs=new_imaging_request_html_attrs,
	# 		allow_sort=False,column_html_attrs=column_html_attrs))

	# processing_request_subtable_options = {
	# 'table_id':f'processing_requests',
	# 'border':True,
	# }

	# processing_requests_subtable_class = create_table('processing_request_subtable',
	# 	options=processing_request_subtable_options)
	# processing_request_url_kwargs = {'username':'username',
	# 	'request_name':'request_name','sample_name':'sample_name',
	# 	'imaging_request_number':'imaging_request_number',
	# 	'processing_request_number':'processing_request_number'}
	# processing_requests_subtable_class.add_column('processing_request_number',
	# 	ProcessingRequestLinkCol('processing request number','processing.processing_table',
	# 		url_kwargs=processing_request_url_kwargs,
	# 		column_html_attrs=column_html_attrs))
	# processing_requests_subtable_class.add_column('processor',
	# 	NotAssignedCol('processor',
	# 	column_html_attrs=column_html_attrs))
	# processing_requests_subtable_class.add_column('processing_progress',
	# 	Col('processing progress',
	# 	column_html_attrs=column_html_attrs))
	# processing_requests_subtable_class.add_column('visualization',
	# 	LinkCol('Viz', 'neuroglancer.general_data_setup',
	# 		url_kwargs=processing_request_url_kwargs,
	# 		allow_sort=False,
	# 		column_html_attrs=column_html_attrs))
	# processing_url_kwargs = {'username':'username','request_name':'request_name',
	# 'sample_name':'sample_name','imaging_request_number':'imaging_request_number'}
	# new_processing_request_tooltip_text = ('Not available for archival requests. '
	# 	'Please only request additional processing for this sample and imaging request '
	# 	'if your original request did not cover the sufficient processing. '
	# 	 'To see what processing you have already requested, '
	# 	 'click on the existing processing request number(s) corresponding to this imaging request. '
	# 	 'If this field shows "N/A" it is because no processing is possible for this sample.')
	# new_processing_request_html_attrs = {'class':'infolink','title':new_processing_request_tooltip_text}
	
	# imaging_requests_subtable_class.add_column('new processing request',
	# 	NewProcessingRequestLinkCol('request additional processing','processing.new_processing_request',
	# 		url_kwargs=processing_url_kwargs,th_html_attrs=new_processing_request_html_attrs,
	# 		column_html_attrs=column_html_attrs))
	# imaging_requests_subtable_class.add_column('processing_requests',
	# 	NestedTableCol('Processing Requests',processing_requests_subtable_class))

	# table_class.add_column('imaging_requests',
	# 	NestedTableCol('Imaging Requests',imaging_requests_subtable_class,
	# 		allow_sort=False))
	
	# sorted_contents = sorted(contents,
	# 		key=partial(table_sorter,sort_key=sort),reverse=reverse)
	table = table_class(contents)
	table.sort_by = sort
	table.sort_reverse = reverse
	
	return table 