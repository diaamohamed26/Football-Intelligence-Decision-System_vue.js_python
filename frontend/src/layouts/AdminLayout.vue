<template>
  <div class="min-h-screen bg-[#070A0F]">
    <AdminSidebar />

    <div class="min-h-screen pl-64">
      <AdminHeader />

      <main class="p-4 sm:p-6 lg:p-8">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import AdminHeader from '@/components/admin/AdminHeader.vue'
import AdminSidebar from '@/components/admin/AdminSidebar.vue'
</script>