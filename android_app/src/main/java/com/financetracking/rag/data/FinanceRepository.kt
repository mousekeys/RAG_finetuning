package com.financetracking.rag.data

import com.financetracking.rag.network.ApiClient
import com.financetracking.rag.network.DocumentInput
import com.financetracking.rag.network.QueryInput
import com.financetracking.rag.network.QueryResponse
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * Repository for handling data operations
 */
class FinanceRepository {
    
    private val apiService = ApiClient.apiService
    
    suspend fun checkHealth(): Result<String> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.getHealth()
            if (response.isSuccessful) {
                Result.success(response.body()?.status ?: "Unknown")
            } else {
                Result.failure(Exception("Health check failed: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun addDocument(
        text: String,
        category: String,
        amount: Double? = null,
        date: String? = null
    ): Result<String> = withContext(Dispatchers.IO) {
        try {
            val document = DocumentInput(text, category, amount, date)
            val response = apiService.addDocument(document)
            if (response.isSuccessful) {
                Result.success(response.body()?.message ?: "Document added")
            } else {
                Result.failure(Exception("Failed to add document: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun queryDocuments(query: String): Result<QueryResponse> = withContext(Dispatchers.IO) {
        try {
            val queryInput = QueryInput(query)
            val response = apiService.queryDocuments(queryInput)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Query failed: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun getDocumentCount(): Result<Int> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.getDocumentCount()
            if (response.isSuccessful) {
                Result.success(response.body()?.count ?: 0)
            } else {
                Result.failure(Exception("Failed to get count: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun clearAllDocuments(): Result<String> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.clearDocuments()
            if (response.isSuccessful) {
                Result.success(response.body()?.message ?: "Documents cleared")
            } else {
                Result.failure(Exception("Failed to clear documents: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
