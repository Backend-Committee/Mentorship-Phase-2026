import { SignIn } from '@clerk/clerk-react'

function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Welcome Back</h1>
          <p className="mt-2 text-gray-600">Please sign in to view your reports</p>
        </div>
        <SignIn routing="path" path="/login" redirectUrl="/reports" />
      </div>
    </div>
  )
}

export default LoginPage
