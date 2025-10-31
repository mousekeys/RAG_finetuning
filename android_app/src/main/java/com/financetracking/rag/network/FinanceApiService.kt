package com.financetracking.rag.network

import retrofit2.Response
import retrofit2.http.*

/**
 * API interface for the RAG Finance Tracking backend
 */
interface FinanceApiService {
    
    @GET("/")
    suspend fun getRoot(): Response<RootResponse>
    
    @GET("/health")
    suspend fun getHealth(): Response<HealthResponse>
    
    @POST("/documents/add")
    suspend fun addDocument(@Body document: DocumentInput): Response<DocumentResponse>
    
    @POST("/query")
    suspend fun queryDocuments(@Body query: QueryInput): Response<QueryResponse>
    
    @GET("/documents/count")
    suspend fun getDocumentCount(): Response<DocumentCountResponse>
    
    @DELETE("/documents/clear")
    suspend fun clearDocuments(): Response<ClearResponse>
}

// Request/Response Models
data class RootResponse(
    val message: String,
    val status: String,
    val version: String
)

data class HealthResponse(
    val status: String,
    val timestamp: String
)

data class DocumentInput(
    val text: String,
    val category: String,
    val amount: Double? = null,
    val date: String? = null,
    val metadata: Map<String, Any>? = null
)

data class DocumentResponse(
    val status: String,
    val message: String,
    val id: String
)

data class QueryInput(
    val query: String,
    val n_results: Int = 5
)

data class QueryResponse(
    val answer: String,
    val relevant_documents: List<RelevantDocument>,
    val timestamp: String
)

data class RelevantDocument(
    val text: String,
    val metadata: Map<String, Any>?,
    val distance: Double?
)

data class DocumentCountResponse(
    val count: Int,
    val collection: String
)

data class ClearResponse(
    val status: String,
    val message: String
)
