<script setup lang="ts">
import { RouterView } from 'vue-router'

import Navbar from '@/components/layout/Navbar.vue'
import Footer from '@/components/layout/Footer.vue'
</script>

<template>
  <div class="min-h-screen bg-[#070A0F] text-[#F5F7FA]">
    <!-- Navbar -->
    <Navbar />

    <!-- Page Content -->
    <main class="min-h-[calc(100vh-64px)]">
      <RouterView />
    </main>

    <!-- Footer -->
    <Footer />
  </div>
</template>