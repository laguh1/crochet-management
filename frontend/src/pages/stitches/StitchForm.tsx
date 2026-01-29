import { useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { ArrowLeft, Save } from 'lucide-react'
import { PageContainer } from '@/components/layout'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from '@/components/ui/select'
import { useStitch, useCreateStitch, useUpdateStitch } from '@/hooks'
import {
  STITCH_CATEGORY_LABELS,
  DIFFICULTY_LABELS,
  type StitchCategory,
  type Difficulty
} from '@/types'

const stitchSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  description: z.string().min(1, 'Description is required'),
  abbreviation: z.string().optional().nullable(),
  category: z.string().optional().nullable(),
  difficulty: z.string().optional().nullable(),
  name_es: z.string().optional().nullable(),
  hookfully_link: z.string().optional().nullable(),
  instruction_link: z.string().optional().nullable(),
  video_link: z.string().optional().nullable(),
  notes: z.string().optional().nullable()
})

type StitchFormValues = z.infer<typeof stitchSchema>

export default function StitchForm() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const isEditing = !!id

  const { data: stitch, isLoading: stitchLoading } = useStitch(id || '')
  const createMutation = useCreateStitch()
  const updateMutation = useUpdateStitch()

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors, isSubmitting }
  } = useForm<StitchFormValues>({
    resolver: zodResolver(stitchSchema),
    defaultValues: {
      name: '',
      description: ''
    }
  })

  // Populate form when editing
  useEffect(() => {
    if (stitch) {
      setValue('name', stitch.name)
      setValue('description', stitch.description)
      setValue('abbreviation', stitch.abbreviation)
      setValue('category', stitch.category)
      setValue('difficulty', stitch.difficulty)
      setValue('name_es', stitch.name_es)
      setValue('hookfully_link', stitch.hookfully_link)
      setValue('instruction_link', stitch.instruction_link)
      setValue('video_link', stitch.video_link)
      setValue('notes', stitch.notes)
    }
  }, [stitch, setValue])

  const onSubmit = async (data: StitchFormValues) => {
    const payload = {
      ...data,
      category: (data.category || undefined) as StitchCategory | undefined,
      difficulty: (data.difficulty || undefined) as Difficulty | undefined
    }

    if (isEditing && stitch) {
      // Only include non-form fields from stitch to avoid stale data issues
      await updateMutation.mutateAsync({
        id: stitch.id,
        photos: stitch.photos,
        name_aliases: stitch.name_aliases,  // Preserve name_aliases
        archived: stitch.archived,
        archived_date: stitch.archived_date,
        archived_reason: stitch.archived_reason,
        created_at: stitch.created_at,
        updated_at: stitch.updated_at,
        ...payload
      })
      navigate(`/stitches/${id}`)
    } else {
      const newId = await createMutation.mutateAsync(payload)
      navigate(`/stitches/${newId}`)
    }
  }

  if (isEditing && stitchLoading) {
    return (
      <PageContainer title="Loading...">
        <div className="flex h-64 items-center justify-center text-gray-400">
          Loading stitch...
        </div>
      </PageContainer>
    )
  }

  return (
    <PageContainer
      title={isEditing ? `Edit ${stitch?.name}` : 'New Stitch'}
      actions={
        <Button variant="outline" asChild>
          <Link to={isEditing ? `/stitches/${id}` : '/stitches'}>
            <ArrowLeft className="mr-2 h-4 w-4" />
            Cancel
          </Link>
        </Button>
      }
    >
      <form onSubmit={handleSubmit(onSubmit)} className="max-w-2xl space-y-6">
        {/* Basic Info */}
        <Card>
          <CardHeader>
            <CardTitle>Basic Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <Label htmlFor="name">Name *</Label>
                <Input id="name" {...register('name')} className="mt-1" />
                {errors.name && (
                  <p className="mt-1 text-sm text-red-500">{errors.name.message}</p>
                )}
              </div>
              <div>
                <Label htmlFor="abbreviation">Abbreviation</Label>
                <Input
                  id="abbreviation"
                  placeholder="e.g., sc, dc"
                  {...register('abbreviation')}
                  className="mt-1"
                />
              </div>
            </div>

            <div>
              <Label htmlFor="description">Description *</Label>
              <Textarea
                id="description"
                {...register('description')}
                className="mt-1"
                rows={3}
                placeholder="Describe the stitch and how to work it..."
              />
              {errors.description && (
                <p className="mt-1 text-sm text-red-500">{errors.description.message}</p>
              )}
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <Label>Category</Label>
                <Select
                  value={watch('category') || ''}
                  onValueChange={(v) => setValue('category', v || null)}
                >
                  <SelectTrigger className="mt-1">
                    <SelectValue placeholder="Select..." />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.entries(STITCH_CATEGORY_LABELS).map(([value, label]) => (
                      <SelectItem key={value} value={value}>
                        {label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Difficulty</Label>
                <Select
                  value={watch('difficulty') || ''}
                  onValueChange={(v) => setValue('difficulty', v || null)}
                >
                  <SelectTrigger className="mt-1">
                    <SelectValue placeholder="Select..." />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.entries(DIFFICULTY_LABELS).map(([value, label]) => (
                      <SelectItem key={value} value={value}>
                        {label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div>
              <Label htmlFor="name_es">Spanish Name</Label>
              <Input id="name_es" {...register('name_es')} className="mt-1" />
            </div>
          </CardContent>
        </Card>

        {/* Resources */}
        <Card>
          <CardHeader>
            <CardTitle>Resources</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="hookfully_link">Hookfully Link</Label>
              <Input
                id="hookfully_link"
                type="url"
                placeholder="https://hookfully.com/..."
                {...register('hookfully_link')}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="instruction_link">Instruction Link</Label>
              <Input
                id="instruction_link"
                type="url"
                {...register('instruction_link')}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="video_link">Video Tutorial Link</Label>
              <Input
                id="video_link"
                type="url"
                placeholder="https://youtube.com/..."
                {...register('video_link')}
                className="mt-1"
              />
            </div>
          </CardContent>
        </Card>

        {/* Notes */}
        <Card>
          <CardHeader>
            <CardTitle>Notes</CardTitle>
          </CardHeader>
          <CardContent>
            <Textarea
              {...register('notes')}
              rows={4}
              placeholder="Personal notes about using this stitch..."
            />
          </CardContent>
        </Card>

        {/* Submit */}
        <div className="flex justify-end gap-2">
          <Button type="submit" disabled={isSubmitting}>
            <Save className="mr-2 h-4 w-4" />
            {isSubmitting ? 'Saving...' : isEditing ? 'Save Changes' : 'Create Stitch'}
          </Button>
        </div>
      </form>
    </PageContainer>
  )
}
