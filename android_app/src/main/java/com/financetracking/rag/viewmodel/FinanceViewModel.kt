package com.financetracking.rag.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.financetracking.rag.data.FinanceRepository
import com.financetracking.rag.network.QueryResponse
import com.financetracking.rag.network.RelevantDocument
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

/**
 * ViewModel for managing UI state and business logic
 */
class FinanceViewModel : ViewModel() {
    
    private val repository = FinanceRepository()
    
    private val _uiState = MutableStateFlow<UiState>(UiState.Idle)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()
    
    private val _documentCount = MutableStateFlow(0)
    val documentCount: StateFlow<Int> = _documentCount.asStateFlow()
    
    private val _queryResult = MutableStateFlow<QueryResponse?>(null)
    val queryResult: StateFlow<QueryResponse?> = _queryResult.asStateFlow()
    
    init {
        checkHealth()
        refreshDocumentCount()
    }
    
    fun checkHealth() {
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            repository.checkHealth()
                .onSuccess { status ->
                    _uiState.value = UiState.Success("Backend is $status")
                }
                .onFailure { error ->
                    _uiState.value = UiState.Error("Connection failed: ${error.message}")
                }
        }
    }
    
    fun addDocument(text: String, category: String, amount: String, date: String) {
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            
            val amountDouble = amount.toDoubleOrNull()
            val dateStr = date.ifEmpty { null }
            
            repository.addDocument(text, category, amountDouble, dateStr)
                .onSuccess { message ->
                    _uiState.value = UiState.Success(message)
                    refreshDocumentCount()
                }
                .onFailure { error ->
                    _uiState.value = UiState.Error("Failed to add: ${error.message}")
                }
        }
    }
    
    fun queryDocuments(query: String) {
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            repository.queryDocuments(query)
                .onSuccess { response ->
                    _queryResult.value = response
                    _uiState.value = UiState.QuerySuccess(response)
                }
                .onFailure { error ->
                    _uiState.value = UiState.Error("Query failed: ${error.message}")
                }
        }
    }
    
    fun refreshDocumentCount() {
        viewModelScope.launch {
            repository.getDocumentCount()
                .onSuccess { count ->
                    _documentCount.value = count
                }
                .onFailure {
                    // Silently fail for count updates
                }
        }
    }
    
    fun clearAllDocuments() {
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            repository.clearAllDocuments()
                .onSuccess { message ->
                    _uiState.value = UiState.Success(message)
                    _queryResult.value = null
                    refreshDocumentCount()
                }
                .onFailure { error ->
                    _uiState.value = UiState.Error("Failed to clear: ${error.message}")
                }
        }
    }
    
    fun resetState() {
        _uiState.value = UiState.Idle
    }
}

/**
 * Sealed class representing different UI states
 */
sealed class UiState {
    object Idle : UiState()
    object Loading : UiState()
    data class Success(val message: String) : UiState()
    data class Error(val message: String) : UiState()
    data class QuerySuccess(val response: QueryResponse) : UiState()
}
