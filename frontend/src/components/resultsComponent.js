import Box from '@mui/material/Box';
import { DataGrid } from '@mui/x-data-grid';

function ResultsComponent(props) {
    console.log("RC: Start", props)

    const columns = [
        
        {
            field: 'fine_amount',
            headerName: 'Fine Amount',
            type: 'number',
            flex: 1,
            editable: false,
        },
        {
            field: 'fine_currency',
            headerName: 'Fine Currency',
            flex: 1,
            editable: false,
        },
        {
            field: 'companies',
            headerName: 'Companies',
            flex: 3,
            editable: false,
            renderCell: (params) => {
                return params.value.join(", ")
            },
        },
        {
            field: 'sector',
            headerName: 'Sector',
            flex: 2,
            editable: false,
        },
        {
            field: 'summary',
            headerName: 'Summary',
            flex: 5,
            editable: false,
        },
        {
            field: 'gh_direct_url',
            headerName: 'GDPR Hub Link',
            flex: 1,
            editable: false,
            renderCell: (params) => {
                if(params.value.length === 0) return
                return <a href={params.value} target='_blank' rel="noreferrer">Link</a>
            },
        },
        {
            field: 'et_direct_url',
            headerName: 'GDPR Enforcement Tracker Link',
            flex: 1,
            editable: false,
            renderCell: (params) => {
                if(params.value.length === 0) return
                return <a href={params.value} target='_blank' rel="noreferrer">Link</a>
            },
        },
    ];


    return (
        <div>
            <Box sx={{ height: "100%", width: '100%' }}>
                <DataGrid
                    getRowId={(row) => row.gh_id + '/' + row.et_id}
                    rows={props.data}
                    columns={columns}
                    initialState={{
                        pagination: {
                            paginationModel: {
                                pageSize: 10,
                            },
                        },
                    }}
                    pageSizeOptions={[10]}
                    disableRowSelectionOnClick
                    disableColumnFilter 
                    disableColumnSelector 
                    disableColumnMenu  
                    disableSelectionOnClick  
                />
            </Box>
        </div>
    )
}
export default ResultsComponent;