package com.financetracking.rag.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.financetracking.rag.network.RelevantDocument
import com.financetracking.rag.viewmodel.FinanceViewModel
import com.financetracking.rag.viewmodel.UiState

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FinanceScreen(viewModel: FinanceViewModel = viewModel()) {
    var selectedTab by remember { mutableStateOf(0) }
    val tabs = listOf("Query", "Add Document")
    
    val uiState by viewModel.uiState.collectAsState()
    val documentCount by viewModel.documentCount.collectAsState()
    val queryResult by viewModel.queryResult.collectAsState()
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    Column {
                        Text("RAG Finance Tracker")
                        Text(
                            "Documents: $documentCount",
                            fontSize = 12.sp,
                            color = Color.White.copy(alpha = 0.7f)
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = Color.White
                )
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            // Tab Row
            TabRow(selectedTabIndex = selectedTab) {
                tabs.forEachIndexed { index, title ->
                    Tab(
                        selected = selectedTab == index,
                        onClick = { selectedTab = index },
                        text = { Text(title) }
                    )
                }
            }
            
            // Status Message
            when (uiState) {
                is UiState.Loading -> {
                    LinearProgressIndicator(
                        modifier = Modifier.fillMaxWidth()
                    )
                }
                is UiState.Success -> {
                    Surface(
                        modifier = Modifier.fillMaxWidth(),
                        color = Color(0xFF4CAF50)
                    ) {
                        Text(
                            text = (uiState as UiState.Success).message,
                            color = Color.White,
                            modifier = Modifier.padding(8.dp),
                            textAlign = TextAlign.Center
                        )
                    }
                }
                is UiState.Error -> {
                    Surface(
                        modifier = Modifier.fillMaxWidth(),
                        color = Color(0xFFF44336)
                    ) {
                        Text(
                            text = (uiState as UiState.Error).message,
                            color = Color.White,
                            modifier = Modifier.padding(8.dp),
                            textAlign = TextAlign.Center
                        )
                    }
                }
                else -> {}
            }
            
            // Content
            when (selectedTab) {
                0 -> QueryTab(viewModel, queryResult)
                1 -> AddDocumentTab(viewModel)
            }
        }
    }
}

@Composable
fun QueryTab(viewModel: FinanceViewModel, queryResult: com.financetracking.rag.network.QueryResponse?) {
    var queryText by remember { mutableStateOf("") }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(
            text = "Ask about your finances",
            fontSize = 20.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(bottom = 16.dp)
        )
        
        OutlinedTextField(
            value = queryText,
            onValueChange = { queryText = it },
            label = { Text("Enter your question") },
            placeholder = { Text("e.g., What are my expenses this month?") },
            modifier = Modifier.fillMaxWidth(),
            maxLines = 3
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Button(
                onClick = {
                    if (queryText.isNotEmpty()) {
                        viewModel.queryDocuments(queryText)
                    }
                },
                modifier = Modifier.weight(1f)
            ) {
                Text("Query")
            }
            
            OutlinedButton(
                onClick = { queryText = "" },
                modifier = Modifier.weight(1f)
            ) {
                Text("Clear")
            }
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        
        if (queryResult != null) {
            Text(
                text = "Answer:",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(bottom = 8.dp)
            )
            
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.secondaryContainer
                )
            ) {
                Text(
                    text = queryResult.answer,
                    modifier = Modifier.padding(16.dp)
                )
            }
            
            if (queryResult.relevant_documents.isNotEmpty()) {
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = "Relevant Documents:",
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(bottom = 8.dp)
                )
                
                LazyColumn(
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(queryResult.relevant_documents) { doc ->
                        RelevantDocumentCard(doc)
                    }
                }
            }
        }
    }
}

@Composable
fun RelevantDocumentCard(document: RelevantDocument) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Text(
                text = document.text,
                fontSize = 14.sp
            )
            
            document.metadata?.let { metadata ->
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "Category: ${metadata["category"] ?: "N/A"}",
                    fontSize = 12.sp,
                    color = Color.Gray
                )
                metadata["amount"]?.let { amount ->
                    Text(
                        text = "Amount: $$amount",
                        fontSize = 12.sp,
                        color = Color.Gray
                    )
                }
            }
        }
    }
}

@Composable
fun AddDocumentTab(viewModel: FinanceViewModel) {
    var text by remember { mutableStateOf("") }
    var category by remember { mutableStateOf("") }
    var amount by remember { mutableStateOf("") }
    var date by remember { mutableStateOf("") }
    var expanded by remember { mutableStateOf(false) }
    
    val categories = listOf("Income", "Expense", "Investment", "Savings", "Loan", "Other")
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(
            text = "Add Financial Document",
            fontSize = 20.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(bottom = 16.dp)
        )
        
        OutlinedTextField(
            value = text,
            onValueChange = { text = it },
            label = { Text("Description") },
            placeholder = { Text("e.g., Grocery shopping at Walmart") },
            modifier = Modifier.fillMaxWidth(),
            maxLines = 4
        )
        
        Spacer(modifier = Modifier.height(12.dp))
        
        ExposedDropdownMenuBox(
            expanded = expanded,
            onExpandedChange = { expanded = !expanded }
        ) {
            OutlinedTextField(
                value = category,
                onValueChange = {},
                readOnly = true,
                label = { Text("Category") },
                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                modifier = Modifier
                    .fillMaxWidth()
                    .menuAnchor()
            )
            
            ExposedDropdownMenu(
                expanded = expanded,
                onDismissRequest = { expanded = false }
            ) {
                categories.forEach { cat ->
                    DropdownMenuItem(
                        text = { Text(cat) },
                        onClick = {
                            category = cat
                            expanded = false
                        }
                    )
                }
            }
        }
        
        Spacer(modifier = Modifier.height(12.dp))
        
        OutlinedTextField(
            value = amount,
            onValueChange = { amount = it },
            label = { Text("Amount (optional)") },
            placeholder = { Text("e.g., 125.50") },
            modifier = Modifier.fillMaxWidth()
        )
        
        Spacer(modifier = Modifier.height(12.dp))
        
        OutlinedTextField(
            value = date,
            onValueChange = { date = it },
            label = { Text("Date (optional)") },
            placeholder = { Text("e.g., 2024-01-15") },
            modifier = Modifier.fillMaxWidth()
        )
        
        Spacer(modifier = Modifier.height(24.dp))
        
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Button(
                onClick = {
                    if (text.isNotEmpty() && category.isNotEmpty()) {
                        viewModel.addDocument(text, category, amount, date)
                        // Clear form
                        text = ""
                        category = ""
                        amount = ""
                        date = ""
                    }
                },
                modifier = Modifier.weight(1f),
                enabled = text.isNotEmpty() && category.isNotEmpty()
            ) {
                Text("Add Document")
            }
            
            OutlinedButton(
                onClick = {
                    text = ""
                    category = ""
                    amount = ""
                    date = ""
                },
                modifier = Modifier.weight(1f)
            ) {
                Text("Clear")
            }
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        
        Button(
            onClick = { viewModel.clearAllDocuments() },
            modifier = Modifier.fillMaxWidth(),
            colors = ButtonDefaults.buttonColors(
                containerColor = Color(0xFFF44336)
            )
        ) {
            Text("Clear All Documents")
        }
    }
}
