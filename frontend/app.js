import { createApp } from 'vue'

const app = createApp({
  data() {
    return {
      file: null,
      loading: false,
      result: null,
      error: null,
      apiUrl: 'http://localhost:8000'
    }
  },
  methods: {
    handleFileSelect(event) {
      this.file = event.target.files[0]
      this.error = null
      console.log('File selected:', this.file?.name)
    },
    async handleFileDragOver(event) {
      event.preventDefault()
      event.stopPropagation()
      event.target.classList.add('border-blue-500', 'bg-blue-50')
    },
    async handleFileDragLeave(event) {
      event.preventDefault()
      event.target.classList.remove('border-blue-500', 'bg-blue-50')
    },
    async handleFileDrop(event) {
      event.preventDefault()
      event.stopPropagation()
      event.target.classList.remove('border-blue-500', 'bg-blue-50')
      
      if (event.dataTransfer.files.length > 0) {
        this.file = event.dataTransfer.files[0]
        this.error = null
      }
    },
    async submitFile() {
      if (!this.file) {
        this.error = '❌ Please select a file'
        return
      }
      
      const validFormats = ['.pdf', '.docx', '.txt']
      const fileName = this.file.name.toLowerCase()
      const isValidFormat = validFormats.some(fmt => fileName.endsWith(fmt))
      
      if (!isValidFormat) {
        this.error = `❌ Invalid format. Supported: ${validFormats.join(', ')}`
        return
      }
      
      this.loading = true
      this.error = null
      this.result = null
      
      try {
        const formData = new FormData()
        formData.append('file', this.file)
        
        console.log('Sending request to', this.apiUrl)
        
        const response = await fetch(`${this.apiUrl}/api/anonymize`, {
          method: 'POST',
          body: formData
        })
        
        const data = await response.json()
        
        if (data.status === 'success') {
          this.result = data
          console.log('✓ Success!', data)
        } else {
          this.error = `❌ Error: ${data.detail || data.message || 'Unknown error'}`
          console.error('Error response:', data)
        }
      } catch (err) {
        this.error = `❌ Error: ${err.message}`
        console.error('Fetch error:', err)
      } finally {
        this.loading = false
      }
    },
    resetForm() {
      this.file = null
      this.result = null
      this.error = null
    }
  },
  template: `
    <div class="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 p-4 md:p-8">
      <div class="max-w-3xl mx-auto">
        <!-- Header -->
        <div class="text-center mb-12">
          <h1 class="text-5xl font-bold text-white mb-2">🛡️ DataShield</h1>
          <p class="text-blue-200 text-xl">Document Anonymizer with SLM</p>
          <p class="text-blue-300 text-sm mt-2">Remove personal information instantly</p>
        </div>
        
        <!-- Upload Card -->
        <div class="bg-white rounded-xl shadow-2xl p-8 mb-6">
          <!-- Drag & Drop Zone -->
          <div 
            @dragover="handleFileDragOver"
            @dragleave="handleFileDragLeave"
            @drop="handleFileDrop"
            class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-6
              hover:border-blue-500 hover:bg-blue-50 transition-all cursor-pointer"
          >
            <input 
              type="file" 
              @change="handleFileSelect"
              accept=".pdf,.docx,.txt"
              class="hidden"
              id="fileInput"
            />
            <label for="fileInput" class="cursor-pointer">
              <div class="text-5xl mb-3">📄</div>
              <p class="text-gray-700 font-semibold mb-1">Drag & drop your file here</p>
              <p class="text-gray-500 text-sm">or click to select</p>
              <p class="text-xs text-gray-400 mt-3">Supported: PDF, DOCX, TXT</p>
            </label>
          </div>
          
          <!-- File Info -->
          <div v-if="file" class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <p class="text-sm text-gray-600">
              📁 Selected file: <span class="font-semibold text-gray-800">{{ file.name }}</span>
              ({{ (file.size / 1024).toFixed(2) }} KB)
            </p>
          </div>
          
          <!-- Action Buttons -->
          <div class="flex gap-3">
            <button 
              @click="submitFile"
              :disabled="!file || loading"
              class="flex-1 bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 rounded-lg font-semibold
                hover:from-blue-700 hover:to-blue-800 disabled:opacity-50 disabled:cursor-not-allowed
                transition-all duration-200 flex items-center justify-center gap-2"
            >
              <span v-if="!loading">🔒 Anonymize & Summarize</span>
              <span v-else>⏳ Processing...</span>
            </button>
            <button 
              @click="resetForm"
              class="px-6 bg-gray-200 text-gray-700 py-3 rounded-lg font-semibold
                hover:bg-gray-300 transition-all"
            >
              Reset
            </button>
          </div>
        </div>
        
        <!-- Error Message -->
        <div v-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg mb-6">
          {{ error }}
        </div>
        
        <!-- Results -->
        <div v-if="result" class="space-y-4">
          <!-- Summary -->
          <div class="bg-gradient-to-br from-green-50 to-blue-50 rounded-xl shadow-lg p-6 border border-green-200">
            <div class="flex items-center gap-2 mb-3">
              <span class="text-2xl">📊</span>
              <h3 class="text-lg font-bold text-gray-800">Summary</h3>
            </div>
            <p class="text-gray-700 leading-relaxed">{{ result.summary }}</p>
          </div>
          
          <!-- Anonymized Text -->
          <div class="bg-white rounded-xl shadow-lg p-6 border border-blue-200">
            <div class="flex items-center gap-2 mb-3">
              <span class="text-2xl">🔒</span>
              <h3 class="text-lg font-bold text-gray-800">Anonymized Text</h3>
            </div>
            <div class="bg-gray-50 rounded-lg p-4 max-h-64 overflow-y-auto">
              <p class="text-gray-700 whitespace-pre-wrap text-sm font-mono">{{ result.anonymized_text }}</p>
            </div>
          </div>
          
          <!-- Statistics -->
          <div class="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl shadow-lg p-6 border border-purple-200">
            <div class="flex items-center gap-2 mb-4">
              <span class="text-2xl">📈</span>
              <h3 class="text-lg font-bold text-gray-800">Statistics</h3>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div class="bg-white rounded-lg p-3 text-center border border-purple-100">
                <p class="text-2xl font-bold text-purple-600">{{ result.statistics.original_length }}</p>
                <p class="text-xs text-gray-600 mt-1">Original chars</p>
              </div>
              <div class="bg-white rounded-lg p-3 text-center border border-purple-100">
                <p class="text-2xl font-bold text-blue-600">{{ result.statistics.anonymized_length }}</p>
                <p class="text-xs text-gray-600 mt-1">Anonymized chars</p>
              </div>
              <div class="bg-white rounded-lg p-3 text-center border border-purple-100">
                <p class="text-2xl font-bold text-green-600">{{ result.statistics.compression_ratio }}%</p>
                <p class="text-xs text-gray-600 mt-1">Compression</p>
              </div>
              <div class="bg-white rounded-lg p-3 text-center border border-purple-100">
                <p class="text-2xl font-bold text-orange-600">{{ result.statistics.processing_time_ms }}ms</p>
                <p class="text-xs text-gray-600 mt-1">Time taken</p>
              </div>
            </div>
          </div>
          
          <!-- Original Text Preview -->
          <div class="bg-gray-100 rounded-xl shadow-lg p-6 border border-gray-300">
            <div class="flex items-center gap-2 mb-3">
              <span class="text-2xl">📝</span>
              <h3 class="text-lg font-bold text-gray-800">Original (Preview)</h3>
            </div>
            <div class="bg-white rounded-lg p-4 max-h-48 overflow-y-auto border border-gray-200">
              <p class="text-gray-700 whitespace-pre-wrap text-sm">{{ result.original_text }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})

app.mount('#app')